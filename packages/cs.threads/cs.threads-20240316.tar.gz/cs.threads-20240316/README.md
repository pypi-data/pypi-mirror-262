Thread related convenience classes and functions.

*Latest release 20240316*:
Fixed release upload artifacts.

## Class `AdjustableSemaphore`

A semaphore whose value may be tuned after instantiation.

*Method `AdjustableSemaphore.acquire(self, blocking=True)`*:
The acquire() method calls the base acquire() method if not blocking.
If blocking is true, the base acquire() is called inside a lock to
avoid competing with a reducing adjust().

*Method `AdjustableSemaphore.adjust(self, newvalue)`*:
Set capacity to `newvalue`
by calling release() or acquire() an appropriate number of times.

If `newvalue` lowers the semaphore capacity then adjust()
may block until the overcapacity is released.

*Method `AdjustableSemaphore.adjust_delta(self, delta)`*:
Adjust capacity by `delta` by calling release() or acquire()
an appropriate number of times.

If `delta` lowers the semaphore capacity then adjust() may block
until the overcapacity is released.

*Method `AdjustableSemaphore.release(self)`*:
Release the semaphore.

## Function `bg(func, daemon=None, name=None, no_start=False, no_logexc=False, thread_class=None, thread_states=None, args=None, kwargs=None)`

Dispatch the callable `func` in its own `Thread`;
return the `Thread`.

Parameters:
* `func`: a callable for the `Thread` target.
* `daemon`: optional argument specifying the `.daemon` attribute.
* `name`: optional argument specifying the `Thread` name,
  default: the name of `func`.
* `no_logexc`: if false (default `False`), wrap `func` in `@logexc`.
* `no_start`: optional argument, default `False`.
  If true, do not start the `Thread`.
* `thread_class`: the `Thread` factory, default `HasThreadState.Thread`
* `thread_states`: passed tothe  `thread_class` factory
* `args`, `kwargs`: passed to the `Thread` constructor

## Class `HasThreadState(cs.context.ContextManagerMixin)`

A mixin for classes with a `cs.threads.ThreadState` instance as `.state`
providing a context manager which pushes `current=self` onto that state
and a `default()` class method returning `cls.perthread_state.current`
as the default instance of that class.

*NOTE*: the documentation here refers to `cls.perthread_state`, but in
fact we honour the `cls.THREAD_STATE_ATTR` attribute to name
the state attribute which allows perclass state attributes,
and also use with classes which already use `.perthread_state` for
another purpose.

*NOTE*: `HasThreadState.Thread` is a _class_ method whose default
is to push state for all active `HasThreadState` subclasses.
Contrast with `HasThreadState.bg` which is an _instance_method
whose default is to push state for just that instance.
The top level `cs.threads.bg` function calls `HasThreadState.Thread`
to obtain its `Thread`.

*Method `HasThreadState.Thread(*Thread_a, target, thread_states=None, **Thread_kw)`*:
Class factory for a `Thread` to push the `.current` state for this class.

The optional parameter `thread_states`
may be used to pass an explicit mapping of `type`->`instance`
of thread states to use;
the default states come from `HasThreadState.get_thread_states()`.
The values of this mapping are iterated over and used as context managers.

A boolean value may also be passed meaning:
* `False`: do not apply any thread states
* `True`: apply the default thread states

Note: the default `thread_states` does a `with current:`
for this class' `current` instance (if any) so that the
`Thread` holds it open until completed.
For some worker threads such as `MultiOpenMixin`s consuming
a queue of tasks this may be undesirable if the instance
shutdown phase includes a close-and-drain for the queue -
because the `Thread` holds the instance open, the shutdown
phase never arrives.
In this case, pass `thread_states=False` to this call.

*Method `HasThreadState.__enter_exit__(self)`*:
Push `self.perthread_state.current=self` as the `Thread` local current instance.

Include `self.__class__` in the set of currently active classes for the duration.

*Method `HasThreadState.bg(self, func, *bg_a, thread_states=None, **bg_kw)`*:
Get a `Thread` using `self.Thread` and start it.
Return the `Thread`.

Note: the default `thread_states` is `{type(self): self}`
in order to arranges a `with self:` so that the `Thread`
holds it open until completed.
For some worker threads such as `MultiOpenMixin`s consuming
a queue of tasks this may be undesirable if the instance
shutdown phase includes a close-and-drain for the queue -
because the `Thread` holds the instance open, the shutdown
phase never arrives.
In this case, pass `thread_states=False` to this call.

*Method `HasThreadState.default(factory=None, raise_on_None=False)`*:
The default instance of this class from `cls.perthread_state.current`.

Parameters:
* `factory`: optional callable to create an instance of `cls`
  if `cls.perthread_state.current` is `None` or missing;
  if `factory` is `True` then `cls` is used as the factory
* `raise_on_None`: if `cls.perthread_state.current` is `None` or missing
  and `factory` is false and `raise_on_None` is true,
  raise a `RuntimeError`;
  this is primarily a debugging aid

*Method `HasThreadState.get_thread_states(all_classes=None)`*:
Return a mapping of `class`->*current_instance*`
for use with `HasThreadState.with_thread_states`
or `HasThreadState.Thread` or `HasThreadState.bg`.

The default behaviour returns just a mapping for this class,
expecting the default instance to be responsible for what
other resources it holds.

There is also a legacy mode for `all_classes=True`
where the mapping is for all active classes,
probably best used for `Thread`s spawned outside
a `HasThreadState` context.

Parameters:
* `all_classes`: optional flag, default `False`;
  if true, return a mapping of class to current instance
  for all `HasThreadState` subclasses with an open instance,
  otherwise just a mapping from this class to its current instance

*Method `HasThreadState.with_thread_states(thread_states: Optional[Mapping[type, Any]] = None)`*:
Context manager to push all the current objects from `thread_states`
by calling each as a context manager.

The default `thread_states` comes from `HasThreadState.get_thread_states()`.

## Function `joinif(T: threading.Thread)`

Call `T.join()` if `T` is not the current `Thread`.

Unlike `threading.Thread.join`, this function is a no-op if
`T` is the current `Thread.

The use case is situations such as the shutdown phase of the
`MultiOpenMixin.startup_shutdown` context manager. Because
the "initial open" startup phase is not necessarily run in
the same thread as the "final close" shutdown phase, it is
possible for example for a worker `Thread` to execute the
shutdown phase and try to join itself. Using this function
allows that scenario.

## Class `LockableMixin`

Trite mixin to control access to an object via its `._lock` attribute.
Exposes the `._lock` as the property `.lock`.
Presents a context manager interface for obtaining an object's lock.

*Method `LockableMixin.__exit__(self, exc_type, exc_value, traceback)`*:
pylint: disable=unused-argument

*Property `LockableMixin.lock`*:
Return the lock.

## Function `locked(*da, **dkw)`

A decorator for instance methods that must run within a lock.

Decorator keyword arguments:
* `initial_timeout`:
  the initial lock attempt timeout;
  if this is `>0` and exceeded a warning is issued
  and then an indefinite attempt is made.
  Default: `2.0`s
* `lockattr`:
  the name of the attribute of `self`
  which references the lock object.
  Default `'_lock'`

## Function `locked_property(*da, **dkw)`

A thread safe property whose value is cached.
The lock is taken if the value needs to computed.

The default lock attribute is `._lock`.
The default attribute for the cached value is `._`*funcname*
where *funcname* is `func.__name__`.
The default "unset" value for the cache is `None`.

## Function `monitor(*da, **dkw)`

Turn a class into a monitor, all of whose public methods are `@locked`.

This is a simple approach which requires class instances to have a
`._lock` which is an `RLock` or compatible
because methods may naively call each other.

Parameters:
* `attrs`: optional iterable of attribute names to wrap in `@locked`.
  If omitted, all names commencing with a letter are chosen.
* `initial_timeout`: optional initial lock timeout, default `10.0`s.
* `lockattr`: optional lock attribute name, default `'_lock'`.

Only attributes satifying `inspect.ismethod` are wrapped
because `@locked` requires access to the instance `._lock` attribute.

## Class `PriorityLock`

A priority based mutex which is acquired by and released to waiters
in priority order.

The initialiser sets a default priority, itself defaulting to `0`.

The `acquire()` method accepts an optional `priority` value
which specifies the priority of the acquire request;
lower values have higher priorities.
`acquire` returns a new `PriorityLockSubLock`.

Note that internally this allocates a `threading.Lock` per acquirer.

When `acquire` is called, if the `PriorityLock` is taken
then the acquirer blocks on their personal `Lock`.

When `release()` is called the highest priority `Lock` is released.

Within a priority level `acquire`s are served in FIFO order.

Used as a context manager, the mutex is obtained at the default priority.
The `priority()` method offers a context manager
with a specified priority.
Both context managers return the `PriorityLockSubLock`
allocated by the `acquire`.

*Method `PriorityLock.__init__(self, default_priority=0, name=None)`*:
Initialise the `PriorityLock`.

Parameters:
* `default_priority`: the default `acquire` priority,
  default `0`.
* `name`: optional identifying name

*Method `PriorityLock.__enter__(self)`*:
Enter the mutex as a context manager at the default priority.
Returns the new `Lock`.

*Method `PriorityLock.__exit__(self, *_)`*:
Exit the context manager.

*Method `PriorityLock.acquire(self, priority=None)`*:
Acquire the mutex with `priority` (default from `default_priority`).
Return the new `PriorityLockSubLock`.

This blocks behind any higher priority `acquire`s
or any earlier `acquire`s of the same priority.

*Method `PriorityLock.priority(self, this_priority)`*:
A context manager with the specified `this_priority`.
Returns the new `Lock`.

*Method `PriorityLock.release(self)`*:
Release the mutex.

Internally, this releases the highest priority `Lock`,
allowing that `acquire`r to go forward.

## Class `PriorityLockSubLock(PriorityLockSubLock, builtins.tuple)`

The record for the per-`acquire`r `Lock` held by `PriorityLock.acquire`.

## Class `State(_thread._local)`

A `Thread` local object with attributes
which can be used as a context manager to stack attribute values.

Example:

    from cs.threads import ThreadState

    S = ThreadState(verbose=False)

    with S(verbose=True) as prev_attrs:
        if S.verbose:
            print("verbose! (formerly verbose=%s)" % prev_attrs['verbose'])

*Method `State.__init__(self, **kw)`*:
Initiale the `ThreadState`, providing the per-Thread initial values.

*Method `State.__call__(self, **kw)`*:
Calling a `ThreadState` returns a context manager which stacks some state.
The context manager yields the previous values
for the attributes which were stacked.

## Class `ThreadState(_thread._local)`

A `Thread` local object with attributes
which can be used as a context manager to stack attribute values.

Example:

    from cs.threads import ThreadState

    S = ThreadState(verbose=False)

    with S(verbose=True) as prev_attrs:
        if S.verbose:
            print("verbose! (formerly verbose=%s)" % prev_attrs['verbose'])

*Method `ThreadState.__init__(self, **kw)`*:
Initiale the `ThreadState`, providing the per-Thread initial values.

*Method `ThreadState.__call__(self, **kw)`*:
Calling a `ThreadState` returns a context manager which stacks some state.
The context manager yields the previous values
for the attributes which were stacked.

## Function `via(cmanager, func, *a, **kw)`

Return a callable that calls the supplied `func` inside a
with statement using the context manager `cmanager`.
This intended use case is aimed at deferred function calls.

# Release Log



*Release 20240316*:
Fixed release upload artifacts.

*Release 20240303*:
* HasThreadState: rename thread_states() to get_thread_states().
* HasThreadState.get_thread_states: some logic fixes.

*Release 20231129*:
* HasThreadState.thread_states: *policy change*: the default now makes a mapping only for this class, not for all HasThreadState subclasses, on the premise that this class can manage use of other classes if required.
* HasThreadState: new bg() class method like Thread() but also starting the Thread.

*Release 20230331*:
* HasThreadState: new thread_states() method to snapshot the current states.
* HasThreadState: new with_thread_states() context manager to apply a set of states.
* HasThreadState: rename the default state from .state to .perthread_state.
* HasThreadState.__enter_exit__: pass cls._HasThreadState_lock to stackset as the modification guard lock, prevents race in thread_states.
* Rename State to ThreadState, which how I always use it anyway, and leave a compatibility name behind.
* New joinif(Thread) method to join a Thread unless we are that Thread - this is because MultiOpenMixin.startup_shutdown stuff may run the shutdown in a differ Thread from that which ran the startup.
* @uses_runstate: use the prevailing RunState or create one.
* Drop Python 2 support.

*Release 20230212*:
* HasThreadState: maintain a set of the HasThreadState classes in use.
* New HasThreadState.Thread class factory method to create a new Thread with the current threads states at time of call instantiated in the new Thread.
* bg: new no_context=False parameter to suppress use of HasThreadState.Thread to create the new Thread.

*Release 20230125*:
New HasThreadState mixin for classes with a state=State() attribute to provide a cls.default() class method for the default instance and a context manager to push/pop self.state.current=self.

*Release 20221228*:
* Get error and warning from cs.gimmicks, breaks circular import with cs.logutils.
* Late import of cs.logutils.LogTime to avoid circular import.

*Release 20221207*:
Small bug fix.

*Release 20221118*:
REMOVE WorkerThreadPool, pulls in too many other things and was never used.

*Release 20211208*:
bg: do not pass the current Pfx prefix into the new Thread, seems to leak and grow.

*Release 20210306*:
bg: include the current Pfx prefix in the thread name and thread body Pfx, obsoletes cs.pfx.PfxThread.

*Release 20210123*:
New @monitor class decorator for simple RLock based reentrance protection.

*Release 20201025*:
* @locked: bump the default warning timeout to 10s, was firing too often.
* New State class for thread local state objects with default attribute values and a stacking __call__ context manager.

*Release 20200718*:
@locked: apply the interior __doc__ to the wrapper.

*Release 20200521*:
@locked_property: decorate with @cs.deco.decorator to support keyword arguments.

*Release 20191102*:
@locked: report slow-to-acquire locks, add initial_timeout and lockattr decorator keyword parameters.

*Release 20190923.2*:
Fix annoying docstring typo.

*Release 20190923.1*:
Docstring updates.

*Release 20190923*:
Remove dependence on cs.obj.

*Release 20190921*:
New PriorityLock class for a mutex which releases in (priority,fifo) order.

*Release 20190812*:
bg: compute default name before wrapping `func` in @logexc.

*Release 20190729*:
bg: provide default `name`, run callable inside Pfx, add optional no_logexc=False param preventing @logec wrapper if true.

*Release 20190422*:
bg(): new optional `no_start=False` keyword argument, preventing Thread.start if true

*Release 20190102*:
* Drop some unused classes.
* New LockableMixin, presenting a context manager and a .lock property.

*Release 20160828*:
Use "install_requires" instead of "requires" in DISTINFO.

*Release 20160827*:
* Replace bare "excepts" with "except BaseException".
* Doc updates. Other minor improvements.

*Release 20150115*:
First PyPI release.

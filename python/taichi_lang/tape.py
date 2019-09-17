class Tape:
  def __init__(self, runtime, loss=None):
    self.calls = []
    self.entered = False
    self.gradient_evaluated = False
    self.runtime = runtime
    self.eval_on_exit = loss is not None
  
  def __enter__(self):
    self.runtime.target_tape = self
    assert self.entered == False, "Tape can be entered only once."
    self.entered = True
  
  def __exit__(self, type, value, tb):
    # print('# kernel calls', len(self.calls))
    self.runtime.target_tape = None
    if self.eval_on_exit:
      self.grad(extra_frame_backtrace=1)
  
  def insert(self, func, args):
    self.calls.append((func, args))
  
  def grad(self, extra_frame_backtrace=0):
    assert self.entered == True, "Before evaluating gradiends tape must be entered."
    assert self.gradient_evaluated == False, "Gradients of grad can be evaluated only once."
    for func, args in reversed(self.calls):
      func.grad(extra_frame_backtrace=3 + extra_frame_backtrace, *args)
    self.gradient_evaluated = True

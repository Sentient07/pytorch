# mypy: allow-untyped-defs
import torch
from torch._utils_internal import enable_compiletime_strobelight


if __name__ == "__main__":
    enable_compiletime_strobelight()

    def fn(x, y, z):
        return x * y + z

    @torch.compile()
    def work(n):
        for i in range(3):
            for j in range(5):
                fn(torch.rand(n, n), torch.rand(n, n), torch.rand(n, n))

    # Strobelight will be called only 3 times because dynamo will be disabled after
    # 3rd iteration.
    for i in range(3):
        torch._dynamo.reset()
        work(i)

import random
import time
import openai


def retry_with_exponential_backoff(
        func,
        initial_delay: float = 1,
        exponential_base: float = 2,
        jitter: bool = True,
        max_retries: int = 6,
        errors: tuple = (openai.RateLimitError,),
):
    """
    func:需要被装饰的函数。
    initial_delay:初始延迟时间，用于指定重试的初始等待时间。
    exponential_base:退避算法的底数，用于指定重试延迟时间的指数增长基数。
    jitter:控制是否启用随机抖动，以避免同时重试的请求发生同步冲突。
    max_retries:允许的最大重试次数。
    errors:需要触发重试的错误类型，以元组的形式指定。
    """

    def wrapper(*args, **kwargs):
        num_retries = 0  # 初始重试次数
        delay = initial_delay  # 初始重试时间

        while True:
            try:
                return func(*args, **kwargs)

            except errors as e:
                num_retries += 1

                if num_retries > max_retries:
                    raise Exception(
                        f"你已经超过最大重试数量:{num_retries}.")

                delay *= exponential_base * (1 + jitter * min(random.random(), 0.5)) # random.random() 返回 0-1, 并设置抖动范围
                time.sleep(delay)

            except Exception as e:
                raise e

    return wrapper


# 几种抖动值的设置
#
# 1. 限制抖动范围
# 可以通过乘以一个小于1的因子来限制随机抖动的最大值，例如：
#
# delay *= exponential_base * (1 + min(jitter * random.random(), 0.5)
#
# 2. 使用固定抖动值
# 可以完全移除随机性，改为使用一个固定的抖动值，例如：
#
# delay *= exponential_base * (1 + jitter * 0.1)
# 这里，0.1 是一个固定的抖动值，它不会因随机性而变化。
#
# 3. 动态调整抖动值
# 可以根据重试次数或其他条件动态调整抖动值，例如：
#
# delay *= exponential_base * (1 + jitter * (random.random() * (1 - num_retries / max_retries)))
# 这里，随着重试次数的增加，抖动值会逐渐减小，从而避免在多次重试后出现过长的延迟。
#
# 4. 使用更复杂的退避策略
# 可以考虑使用更复杂的退避策略，如全抖动（full jitter）或半抖动（half jitter），这些策略在退避算法中是常见的：
#
# 全抖动：在最小和最大延迟时间之间随机选择一个值。
# 半抖动：在当前延迟时间和两倍当前延迟时间之间随机选择一个值

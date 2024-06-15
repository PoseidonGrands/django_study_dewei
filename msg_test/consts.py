from enum import Enum


# class MessageType(Enum):
#     info = 'info'
#     warning = 'warning'
#     error = 'error'
#     danger = 'danger'
#
#
# MessageType.info.label = '信息'
# MessageType.warning.label = '警告'
# MessageType.error.label = '错误'
# MessageType.danger.label = '危险'
#
# MessageType.info.color = 'green'
# MessageType.warning.color = 'orange'
# MessageType.error.color = 'gray'
# MessageType.danger.color = 'red'


class MessageType(Enum):
    info = ('info', '信息', 'green')
    warning = ('warning', '警告', 'orange')
    error = ('error', '错误', 'gray')
    danger = ('danger', '危险', 'red')

    # @property
    # def value(self):
    #     return self.value[0]

    @property
    def label(self):
        return self.value[1]

    @property
    def color(self):
        return self.value[2]


SENSITIVE_WORDS = ['你好', '世界']

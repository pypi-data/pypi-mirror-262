"""
Random User-Agent
Copyright: 2022-2024 Ekin Karadeniz (github.com/iamdual)
License: Apache License 2.0
"""
from . import formats, serialization, utils
from .data import platforms_mobile
from .data import generator


# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Sec-CH-UA
# https://wicg.github.io/ua-client-hints/#http-ua-hints
class ClientHints:
    # Type hinting only
    mobile: str
    platform: str
    platform_version: str
    brands: str
    brands_full_version_list: str
    bitness: str
    architecture: str
    model: str
    wow64: str

    def __init__(self, gen: generator.Generator):
        self.__generator = gen
        self.__cache = {}

    def __mobile(self):
        return self.__generator.platform in platforms_mobile

    def __platform(self):
        platform = self.__generator.platform

        if platform == 'ios':
            platform = 'iOS'
        elif platform == 'macos':
            platform = 'macOS'
        else:
            platform = platform.title()

        return platform

    def __platform_version(self):
        if self.__generator.platform == 'windows' and formats.major_version(self.__generator.platform_version) == '10':
            return utils.choice(('10.0.0', '13.0.0'))

        return formats.version(self.__generator.platform_version)

    def __brands(self, full_version_list: bool = False):
        brand_list = [{'brand': 'Not A(Brand', 'version': '99'}]

        if full_version_list:
            browser_version = formats.version(self.__generator.browser_version)
        else:
            browser_version = formats.major_version(self.__generator.browser_version)

        if self.__generator.browser == 'chrome':
            brand_list.append({'brand': 'Chromium', 'version': browser_version})
            brand_list.append({'brand': 'Google Chrome', 'version': browser_version})
        elif self.__generator.browser == 'edge':
            brand_list.append({'brand': 'Chromium', 'version': browser_version})
            brand_list.append({'brand': 'Microsoft Edge', 'version': browser_version})

        return brand_list

    def __bitness(self):
        if self.__generator.platform == 'android':
            return utils.choice(('32', '64', '32', '32'))

        return '64'

    def __architecture(self):
        if self.__generator.platform == 'android' or self.__generator.platform == 'ios':
            return 'arm'
        elif self.__generator.platform == 'macos':
            return utils.choice(('arm', 'x86', 'arm', 'arm'))

        return 'x86'

    def __model(self):
        if 'platform_model' in self.__generator.platform_version:
            return self.__generator.platform_version['platform_model']

        return ''

    def __wow64(self):
        return self.__generator.platform == 'windows'

    def __getattr__(self, name):
        if name in self.__cache:
            return self.__cache[name]

        if name == 'mobile':
            self.__cache[name] = serialization.ch_bool(self.__mobile())
        elif name == 'platform':
            self.__cache[name] = serialization.ch_string(self.__platform())
        elif name == 'platform_version':
            self.__cache[name] = serialization.ch_string(self.__platform_version())
        elif name == 'brands':
            self.__cache[name] = serialization.ch_brand_list(self.__brands())
        elif name == 'brands_full_version_list':
            self.__cache[name] = serialization.ch_brand_list(self.__brands(full_version_list=True))
        elif name == 'bitness':
            self.__cache[name] = serialization.ch_string(self.__bitness())
        elif name == 'architecture':
            self.__cache[name] = serialization.ch_string(self.__architecture())
        elif name == 'model':
            self.__cache[name] = serialization.ch_string(self.__model())
        elif name == 'wow64':
            self.__cache[name] = serialization.ch_bool(self.__wow64())

        return self.__cache[name]

    def __str__(self):
        return self.brands

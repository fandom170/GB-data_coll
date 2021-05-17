import scrapy
from scrapy.http import HtmlResponse
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
import html

from instagram.items import InstagramItem


class InstausersSpider(scrapy.Spider):
    name = 'instaUsers'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']

    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    insta_login = ''
    insta_pwd = ""

    parse_user = 'ggtoys'  # user for connections analyze
    parse_users = ['scalescience', 'ggtoys']

    graphql_url = 'https://www.instagram.com/graphql/query/?'

    query_hash_followers = '5aefa9893005572d237da5068082d8d5'
    query_hash_subscribe = '3dec7e2c57367ef3da3d987d89f9dbc8'

    def parse(self, response: HtmlResponse):
        """Start of parsing chain"""
        csrf_token = self.fetch_csrf_token(response.text)

        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={'username': self.insta_login, 'enc_password': self.insta_pwd},
            headers={'X-CSRFToken': csrf_token}
        )

    def login(self, response: HtmlResponse):
        """Take data about authentication from response from server"""
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            for user in self.parse_users:
                yield response.follow(
                    # f'/{self.parse_user}',
                    f'/{str(user)}',
                    callback=self.user_data_parse,
                    #cb_kwargs={'username': self.parse_user}
                    cb_kwargs={'username':user}
                    )

    def user_data_parse(self, response: HtmlResponse, username):
        """Function take data from the page for further using"""
        user_id = self.fetch_user_id(response.text, username)
        print()
        variables = {'id': user_id,
                     'first': 12}

        params = self.get_url_params(variables)

        url_followers = f'{self.graphql_url}query_hash={self.query_hash_followers}&variables={{{params}}}'  # link to followers
        url_subscribes = f'{self.graphql_url}query_hash={self.query_hash_subscribe}&variables={{{params}}}'  # link to subscribes
        print()
        yield response.follow(
            url_followers,
            callback=self.user_followers_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}
        )

        yield response.follow(
            url_subscribes,
            callback=self.user_subscriptions_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}
        )

    def user_followers_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info.get('has_next_page'):
            variables['after'] = page_info['end_cursor']
            params = self.get_next_page_params(variables)
            url_followers = f'{self.graphql_url}query_hash={self.query_hash_followers}&variables={{{params}}}'
            yield response.follow(
                url_followers,
                callback=self.user_followers_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)})

        followers = j_data.get('data').get('user').get('edge_followed_by').get('edges')
        for follower in followers:
            user_data = follower.get('node')
            item_name = 'followers'
            item = InstagramItem(
                user_id=user_id,
                user_name=username,
                linked_acc_id=user_data.get('id'),
                data_type=item_name,
                linked_acc_name=user_data.get('username'),
                full_name=user_data.get('full_name'),
                profile_pic_url=user_data.get('profile_pic_url'),
                user_data=user_data
            )
            yield item

    def user_subscriptions_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
        print()
        if page_info.get('has_next_page'):
            variables['after'] = page_info['end_cursor']
            params = self.get_next_page_params(variables)
            url_subscriptions = f'{self.graphql_url}query_hash={self.query_hash_subscribe}&variables={{{params}}}'
            print()
            yield response.follow(
                url_subscriptions,
                callback=self.user_subscriptions_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)})
            subscriptions = j_data.get('data').get('user').get('edge_follow').get('edges')
            print()
            for subscription in subscriptions:
                user_data = subscription.get('node')
                item_name = 'subscriptions'
                print()
                item = InstagramItem(
                    user_id=user_id,
                    user_name=username,
                    linked_acc_id=user_data.get('id'),
                    data_type=item_name,
                    linked_acc_name=user_data.get('username'),
                    full_name=user_data.get('full_name'),
                    profile_pic_url=user_data.get('profile_pic_url'),
                    user_data=user_data
                )
                yield item

    def fetch_csrf_token(self, text):
        """Take csrf token from js script in the top of page"""
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        print()
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')

    def get_url_params(self, variables):
        param_line = ''
        for k, v in variables.items():
            param_line += f'"{k}"="{v}"&'
        param_line = param_line[:-1]
        param_line = param_line.replace('=', '%3A').replace('&', '%2C')
        return param_line

    def get_next_page_params(self, variables):
        param_line = ''
        for k, v in variables.items():
            if k == 'first':
                param_line += f'"{k}"={v}&'
            else:
                param_line += f'"{k}"="{v}"&'
        param_line = param_line[:-1]
        print()

        param_line = param_line.replace('&', '%2C')\
            .replace('==', '%3D%3D')\
            .replace('=', '%3A')\
            .replace('{', '%7B')\
            .replace('}', '%7D')\
            .replace('"', '%22')
        return param_line
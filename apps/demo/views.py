from django.shortcuts import render
from django.views import View
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import requests


# Create your views here.


class OauthView(GenericAPIView):
    """
         method: 'post',
            url: 'https://github.com/login/oauth/access_token?' +
            `client_id =${clientID} & ` +
            `client_secret =${clientSecret} & ` +
            `code =${requestToken}
            `,

        headers: {
            accept: 'application/json'
        }

          method: 'get',
  url: `https://api.github.com/user`,
  headers: {
    accept: 'application/json',
    Authorization: `token ${accessToken}`
  }
    """

    def get(self, request, *args, **kwargs):
        code = request.query_params.get('code')
        client_id = '22246585d748d66fdc37'
        client_sceret = '130ef29b6190110bc38e05617b1efbfce50aa9b4'

        url = f'https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_sceret}' \
            f'&code={code}'

        headers = {'Accept': 'application/json'}

        res = requests.post(url=url, headers=headers)
        res_data = res.json()
        print(res_data)
        if 'error' not in res_data:
            print()

        return Response(data={'message':'ok'})

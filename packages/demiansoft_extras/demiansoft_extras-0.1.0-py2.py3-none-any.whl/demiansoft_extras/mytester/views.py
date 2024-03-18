from django.shortcuts import render

font_link = "https://fonts.googleapis.com/css2?" \
            "family=Hahmlet:wght@100;200;300;400;500;600;700;800;900&" \
            "family=Noto+Sans+KR:wght@100;300;400;500;700;900&" \
            "family=Noto+Serif+KR:wght@200;300;400;500;600;700;900&" \
            "family=Open+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,300;1,400;1,500;1,600;1,700;1,800&" \
            "family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500;1,600;1,700&" \
            "family=Gugi&display=swap"


def home(request):
    c = dict()
    c['font_link'] = font_link

    return render(request, 'index.html', c)

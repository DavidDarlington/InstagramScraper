from instagram_scraper.helpers import deep_get


def get_story_media_urls(item):
    urls = []

    video_url = deep_get(item, 'video_resources[-1].src')
    img_url = deep_get(item, 'display_resources[-1].src')

    if video_url:
        urls.append(video_url)

    if img_url:
        urls.append(img_url.split('?')[0])

    return urls

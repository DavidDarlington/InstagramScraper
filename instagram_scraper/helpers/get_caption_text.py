from instagram_scraper.helpers import deep_get


def get_caption_text(item):
    caption_text = deep_get(item, 'caption')
    edge_media_caption_text = deep_get(item, 'edge_media_to_caption.edges[0].node.text')

    if caption_text and isinstance(caption_text, dict):
        caption_text = caption_text['text']
    elif edge_media_caption_text:
        caption_text = edge_media_caption_text

    return caption_text


def has_selected_story_media_types(item, selected_media_types):
    # media_type 1 is image, 2 is video
    media_type = item['media_type'] if 'media_type' in item else None

    if media_type:
        if media_type == 1 and 'story-image' in selected_media_types:
            return True
        elif media_type == 2 and 'story-video' in selected_media_types:
            return True

    typename = item['__typename'] if '__typename' in item else None

    if typename:
        if typename == 'GraphStoryImage' and 'story-image' in selected_media_types:
            return True
        elif typename == 'GraphStoryVideo' and 'story-video' in selected_media_types:
            return True

    return False


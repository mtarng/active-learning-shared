import json


def __build_tag_from_VottImageTag(image_tag):
    return {
        "x1": image_tag.x_min,
        "x2": image_tag.x_max,
        "y1": image_tag.y_min,
        "y2": image_tag.y_max,
        "width": image_tag.image_width,
        "height": image_tag.image_height,
        "tags": image_tag.classification_names
    }


def __build_tag_list_from_VottImageTags(image_tag_list):
    tag_list = []
    for image_tag in image_tag_list:
        tag_list.append(__build_tag_from_VottImageTag(image_tag))
    return tag_list


def __build_frames_data(image_id_to_urls, image_id_to_image_tags):
    frames = {}
    for image_id in image_id_to_image_tags.keys():
        image_file_name = __get_filename_from_fullpath(image_id_to_urls[image_id])
        image_tags = __build_tag_list_from_VottImageTags(image_id_to_image_tags[image_id])
        frames[image_file_name] = image_tags
    return frames


# For download function
def create_starting_vott_json(image_id_to_urls, image_id_to_image_tags, existing_classifications_list):
    # "frames"
    frame_to_tag_list_map = __build_frames_data(image_id_to_urls, image_id_to_image_tags)

    # "inputTags"
    classification_str = ""
    for classification in existing_classifications_list:
        classification_str += classification + ","

    return {
        "frames": frame_to_tag_list_map,
        "inputTags": classification_str,
        "scd": False  # Required for VoTT and image processing? unknown if it's also used for video.
    }


def __get_filename_from_fullpath(filename):
    path_components = filename.split('/')
    return path_components[-1]


def __get_id_from_fullpath(fullpath):
    return int(__get_filename_from_fullpath(fullpath).split('.')[0])


# Returns a list of processed tags for a single frame
def __create_tag_data_list(json_tag_list):
    processed_tags = []
    for json_tag in json_tag_list:
        processed_tags.append(__process_json_tag(json_tag))
    return processed_tags


def __process_json_tag(json_tag):
    return {
        "x1": json_tag['x1'],
        "x2": json_tag['x2'],
        "y1": json_tag['y1'],
        "y2": json_tag['y2'],
        "UID": json_tag["UID"],
        "id": json_tag["id"],
        "type": json_tag["type"],
        "classes": json_tag["tags"],
        "name": json_tag["name"]
    }


# For upload function
def process_vott_json(json):
    all_frame_data = json['frames']

    # Scrub filename keys to only have integer Id, drop path and file extensions.
    id_to_tags_dict = {}
    for full_path_key in sorted(all_frame_data.keys()):
        # Map ID to list of processed tag data
        id_to_tags_dict[__get_id_from_fullpath(full_path_key)] = __create_tag_data_list(all_frame_data[full_path_key])
    all_ids = list(id_to_tags_dict.keys())

    # Remove images with no tags from dict
    for id in all_ids:
        if not id_to_tags_dict[id]:
            del(id_to_tags_dict[id])

    # Do the same with visitedFrames
    visited_ids = sorted(json['visitedFrames'])
    for index, filename in enumerate(visited_ids):
        visited_ids[index] = __get_id_from_fullpath(filename)

    visited_no_tag_ids = sorted(list(set(visited_ids) - set(id_to_tags_dict.keys())))

    # Unvisisted imageIds
    unvisited_ids = sorted(list(set(all_ids) - set(visited_ids)))

    return {
            "totalNumImages" : len(all_ids),
            "numImagesVisted" : len(visited_ids),
            "numImagesVisitedNoTag": len(visited_no_tag_ids),
            "numImagesNotVisted" : len(unvisited_ids),
            "imagesVisited" : visited_ids,
            "imagesNotVisited" : unvisited_ids,
            "imagesVisitedNoTag": visited_no_tag_ids,
            "imageIdToTags": id_to_tags_dict
        }


def main():
    images = {
		"1.png" : {},
		"2.png" : {},
		"3.png" : {},
		"4.png" : {},
		"5.png" : {}
	}
    generated_json = create_starting_vott_json(images)
    print("generating starting default json for vott_parser download")
    print(json.dumps(generated_json))

    print('testing tag creation')
    tag1 = __build_json_tag(122, 171, 122, 191, 488, 512, "uiduiduid", 2, "Rectangle", ["Ford", "Volvo", "BMW"],2)
    print(tag1)
    print(json.dumps(tag1))

    print('testing adding two sets')
    output_json = {
        "frames" : {
            "1.png": [],
            "2.png": [tag1, tag1],
            "3.png": [tag1],
            "4.png": [],
            "5.png": []
        },
        "visitedFrames": []
    }
    print()
    print('bare')
    print(json.dumps(output_json))
    print()
    print("Testing process_vott_json")
    print(json.dumps(process_vott_json(output_json)))
    print()
    print(json.dumps(output_json))

    # tag_data = __get_components_from_json_tag(output_json["frames"]["2"][0])
    # print("tag_data: ---" + str(tag_data))
    # add_tag_to_db('something', 2, (tag_data))


# Currently only used for testing...
# returns a json representative of a tag given relevant components
def __build_json_tag(x1, x2, y1, y2, img_width, img_height, UID, id, type, tags, name):
    return {
        "x1": x1,
        "x2": x2,
        "y1": y1,
        "y2": y2,
        "width": img_width,
        "height": img_height,
        "box" : {
            "x1": x1,
            "x2": x2,
            "y1": y1,
            "y2": y2
        },
        "UID": UID,
        "id": id,
        "type": type,
        "tags": tags,
        "name": name
    }


if __name__ == '__main__':
    main()

import os
import logging

# TODO: Modify this function to return a JSON string that contains a "succeeded" list and a "failed" list.
def copy_images_to_permanent_storage(image_id_url_map, copy_source, copy_destination, blob_service):
    # Create a dictionary to store map of new permanent image URLs to image ID's
    update_urls_dictionary = {}

    # Copy images from temporary to permanent storage and delete them.
    for key, value in image_id_url_map.items():
        original_image_url = key
        original_blob_name = original_image_url.split("/")[-1]
        file_extension = os.path.splitext(original_image_url)[1]
        image_id = value
        new_blob_name = (str(image_id) + file_extension)

        # Verbose logging for testing
        logging.debug("Original image name: " + original_blob_name)
        logging.debug("Image ID: " + str(image_id))
        logging.debug("New blob name: " + new_blob_name)

        # Create the blob URLs
        source_blob_path = blob_service.make_blob_url(copy_source, original_blob_name)
        destination_blob_path = blob_service.make_blob_url(copy_destination, new_blob_name)

        # Copy blob from temp storage to permanent storage
        try:
            logging.debug("Now copying file from temporary to permanent storage...")
            logging.debug("Source path: " + source_blob_path)
            logging.debug("Destination path: " + destination_blob_path)
            blob_service.copy_blob(copy_destination, new_blob_name, source_blob_path)
            logging.debug("Done.")

            # Add ImageId and permanent storage url to new dictionary to be sent to update function
            update_urls_dictionary[image_id] = destination_blob_path

            # Delete the file from temp storage once it's been copied
            logging.debug("Now deleting image " + original_blob_name + " from temp storage container.")
            try:
                blob_service.delete_blob(copy_source, original_blob_name)
                logging.debug("Blob " + original_blob_name + " has been deleted successfully")
            except Exception as e:
                logging.error("ERROR: Deletion of blob " + original_blob_name + " failed. Exception: " + str(e))
                update_urls_dictionary.clear()
                return update_urls_dictionary

        except Exception as e:
            logging.error("ERROR: Copy of blob " + original_blob_name + " failed.  Exception: " + str(e))
            update_urls_dictionary.clear()
            return update_urls_dictionary

    return update_urls_dictionary

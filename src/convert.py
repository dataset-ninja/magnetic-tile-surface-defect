# https://github.com/abin24/Magnetic-tile-defect-datasets.

import glob
import os
import shutil
from urllib.parse import unquote, urlparse

import numpy as np
import supervisely as sly
from cv2 import connectedComponents
from dataset_tools.convert import unpack_if_archive
from dotenv import load_dotenv
from supervisely.io.fs import get_file_name, get_file_name_with_ext, get_file_size
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # project_name = "Magnetic tile defect"
    dataset_path = "/home/grokhi/supervisely/repos/Magnetic-tile-defect-datasets."
    ds_name = "ds"
    batch_size = 30
    images_ext = ".jpg"
    masks_ext = ".png"

    def create_ann(image_path):
        labels = []

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        subfolder = image_path.split("/")[-3]
        obj_class = subfolder_to_class.get(subfolder)

        mask_path = image_path.replace(images_ext, masks_ext)
        ann_np = sly.imaging.image.read(mask_path)[:, :, 2]
        mask = ann_np != 0
        ret, curr_mask = connectedComponents(mask.astype("uint8"), connectivity=8)
        for i in range(1, ret):
            obj_mask = curr_mask == i
            curr_bitmap = sly.Bitmap(obj_mask)
            if curr_bitmap.area > 10:
                curr_label = sly.Label(curr_bitmap, obj_class)
                labels.append(curr_label)

        tagval = int(get_file_name(image_path).split("_")[0].split("exp")[-1])
        tags = [sly.Tag(tag_experiment, tagval)]

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    crack = sly.ObjClass("crack", sly.Bitmap)
    blowhole = sly.ObjClass("blowhole", sly.Bitmap)
    break_class = sly.ObjClass("break", sly.Bitmap)
    fray = sly.ObjClass("fray", sly.Bitmap)
    uneven = sly.ObjClass("uneven", sly.Bitmap)

    tag_experiment = sly.TagMeta("experiment", sly.TagValueType.ANY_NUMBER)

    subfolder_to_class = {
        "MT_Blowhole": blowhole,
        "MT_Break": break_class,
        "MT_Crack": crack,
        "MT_Fray": fray,
        "MT_Uneven": uneven,
    }

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=[crack, blowhole, break_class, fray, uneven], tag_metas=[tag_experiment]
    )
    api.project.update_meta(project.id, meta.to_json())

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    images_pathes = glob.glob(dataset_path + "/*/*/*.jpg")

    progress = sly.Progress("Create dataset {}".format(ds_name), len(images_pathes))

    for img_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
        img_names_batch = [get_file_name_with_ext(im_path) for im_path in img_pathes_batch]

        img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns = [create_ann(image_path) for image_path in img_pathes_batch]
        api.annotation.upload_anns(img_ids, anns)

        progress.iters_done_report(len(img_names_batch))
    return project

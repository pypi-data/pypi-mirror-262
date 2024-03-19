from typing import Optional, List, Union
from dataclasses import dataclass

from dataclass_wizard import JSONWizard


@dataclass
class R34Post(JSONWizard):
    # raw: Optional[dict]  # Iterable
    preview_url: str
    sample_url: str
    file_url: str
    # file_type: str
    directory: int
    hash: str
    width: int
    height: int
    id: int
    image: str
    change: int
    owner: str
    parent_id: Union[str, int]
    rating: str
    sample: Optional[bool]
    sample_height: int
    sample_width: int
    score: int
    tags: List[str]
    source: str
    status: str
    has_notes: Optional[bool]
    comment_count: int

    # @staticmethod
    # def from_json(json):
    #     pFileUrl = json["file_url"]
    #     file_type = "video" if pFileUrl.endswith(".mp4") else "gif" if pFileUrl.endswith(".gif") else "image"
    #
    #     return R34Post(
    #         json,
    #         json["preview_url"],
    #         json["sample_url"],
    #         json["file_url"],
    #         file_type,
    #         json["directory"],
    #         json["hash"],
    #         json["width"],
    #         json["height"],
    #         json["id"],
    #         json["image"],
    #         json["change"],
    #         json["owner"],
    #         json["parent_id"],
    #         json["rating"],
    #         json["sample"],
    #         json["sample_height"],
    #         json["sample_width"],
    #         json["score"],
    #         json["tags"].split(" "),
    #         json["source"],
    #         json["status"],
    #         json["has_notes"],
    #         json["comment_count"],
    #     )


@dataclass
class R34Pool(JSONWizard):
    id: int
    link: str
    thumbnails: str
    tags: str


@dataclass
class R34PostComment(JSONWizard):
    created_at: str
    post_id: int
    body: str
    creator: str
    id: int
    creator_id: int


@dataclass
class R34Stats(JSONWizard):
    place: str
    amount: int
    username: str


@dataclass
class R34TopCharacters(JSONWizard):
    name: str
    # url = str
    count: int

    @property
    def url(self) -> str:
        return "https://rule34.xxx/index.php?page=post&s=list&tags={0}".format(self.name.replace(" ", "_"))


@dataclass
class R34TopTag(JSONWizard):
    rank: int
    name: str
    percentage: int


@dataclass
class UserFavorite(JSONWizard):
    id: int
    tags: str
    rating: str
    score: int
    user: str

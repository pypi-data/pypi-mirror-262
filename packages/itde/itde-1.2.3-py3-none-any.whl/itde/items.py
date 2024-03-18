from datetime import date
from datetime import time
from typing import List
from typing import Optional
from .endpoints import Endpoint
from .ytypes import ItemType


class Item:
    def __init__(
        self,
        name: str,
        thumbnail_url: str,
        endpoint: Optional[Endpoint] = None,
        description: Optional[str] = None,
    ) -> None:
        self.name = name
        self.thumbnail_url = thumbnail_url
        self.endpoint = endpoint
        self.description = description
        self.item_type: Optional[ItemType] = None

    def __repr__(self) -> str:
        return (
            "Item{"
            f"item_type={self.item_type}, "
            f"name={self.name}, "
            f"endpoint={self.endpoint}, "
            f"thumbnail_url={self.thumbnail_url}, "
            f"description={self.description}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Item):
            return (
                self.name == __value.name
                and self.thumbnail_url == __value.thumbnail_url
                and self.endpoint == __value.endpoint
                and self.description == __value.description
                and self.item_type == __value.item_type
            )
        else:
            return False

    def __hash__(self):
        return hash(
            (
                self.name,
                self.thumbnail_url,
                self.endpoint,
                self.description,
                self.item_type
            )
        )


class ArtistItem(Item):
    def __init__(self, subscribers: Optional[int] = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.subscribers = subscribers
        self.item_type = ItemType.ARTIST

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + f", subscribers={self.subscribers}" "}"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, ArtistItem):
            return (
                self.name == __value.name
                and self.thumbnail_url == __value.thumbnail_url
                and self.endpoint == __value.endpoint
                and self.description == __value.description
                and self.item_type == __value.item_type
                and self.subscribers == __value.subscribers
            )
        else:
            return False

    def __hash__(self):
        return hash(
            (
                self.name,
                self.thumbnail_url,
                self.endpoint,
                self.description,
                self.item_type,
                self.subscribers,
            )
        )


class VideoItem(Item):
    def __init__(
        self,
        length: Optional[time] = None,
        views: Optional[int] = None,
        artist_items: Optional[List] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        if artist_items is None:
            artist_items = []
        self.length = length
        self.views = views
        self.artist_items = artist_items
        self.item_type = ItemType.VIDEO

    def __repr__(self) -> str:
        return (
            super().__repr__()[:-1] + f", length={self.length}"
            f", views={self.views}"
            f", artist_items={self.artist_items}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, VideoItem):
            return (
                self.name == __value.name
                and self.thumbnail_url == __value.thumbnail_url
                and self.endpoint == __value.endpoint
                and self.description == __value.description
                and self.item_type == __value.item_type
                and self.length == __value.length
                and self.views == __value.views
                and self.artist_items == __value.artist_items
            )
        else:
            return False

    def __hash__(self):
        return hash(
            (
                self.name,
                self.thumbnail_url,
                self.endpoint,
                self.description,
                self.item_type,
                self.length,
                self.views,
                self.artist_items,
            )
        )


class AlbumItem(Item):
    def __init__(
        self,
        release_year: Optional[int] = None,
        length: Optional[time] = None,
        tracks_num: Optional[int] = None,
        artist_items: List[ArtistItem] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        if artist_items is None:
            artist_items = []
        self.length = length
        self.tracks_num = tracks_num
        self.release_year = release_year
        self.artist_items = artist_items
        self.item_type = ItemType.ALBUM

    def __repr__(self) -> str:
        return (
            super().__repr__()[:-1] + f", release_year={self.release_year}"
            f", artist_items={self.artist_items}"
            f", length={self.length}"
            f", tracks_num={self.tracks_num}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, AlbumItem):
            return (
                self.name == __value.name
                and self.thumbnail_url == __value.thumbnail_url
                and self.endpoint == __value.endpoint
                and self.description == __value.description
                and self.item_type == __value.item_type
                and self.length == __value.length
                and self.tracks_num == __value.tracks_num
                and self.release_year == __value.release_year
                and self.artist_items == __value.artist_items
            )
        else:
            return False

    def __hash__(self):
        return hash(
            (
                self.name,
                self.thumbnail_url,
                self.endpoint,
                self.description,
                self.item_type,
                self.length,
                self.tracks_num,
                self.release_year,
                self.artist_items,
            )
        )


class EPItem(AlbumItem):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.item_type = ItemType.EP


class PlaylistItem(AlbumItem):
    def __init__(self, views: Optional[int] = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.views = views
        self.item_type = ItemType.PLAYLIST

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + f", views={self.views}" "}"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, PlaylistItem):
            return (
                self.name == __value.name
                and self.thumbnail_url == __value.thumbnail_url
                and self.endpoint == __value.endpoint
                and self.description == __value.description
                and self.item_type == __value.item_type
                and self.views == __value.views
                and self.length == __value.length
                and self.tracks_num == __value.tracks_num
                and self.release_year == __value.release_year
                and self.artist_items == __value.artist_items
            )
        else:
            return False

    def __hash__(self):
        return hash(
            (
                self.name,
                self.thumbnail_url,
                self.endpoint,
                self.description,
                self.item_type,
                self.views,
                self.length,
                self.tracks_num,
                self.release_year,
                self.artist_items,
            )
        )


class SingleItem(AlbumItem):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.item_type = ItemType.SINGLE


class SongItem(Item):
    def __init__(
        self,
        length: Optional[time] = None,
        reproductions: Optional[int] = None,
        album_item: Optional[AlbumItem] = None,
        artist_items: List[ArtistItem] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        if artist_items is None:
            artist_items = []
        self.length = length
        self.reproductions = reproductions
        self.album_item = album_item
        self.artist_items = artist_items
        self.item_type = ItemType.SONG

    def __repr__(self) -> str:
        return (
            super().__repr__()[:-1] + f", length={self.length}"
            f", reproductions={self.reproductions}"
            f", album_item={self.album_item}"
            f", artist_items={self.artist_items}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, SongItem):
            return (
                self.name == __value.name
                and self.thumbnail_url == __value.thumbnail_url
                and self.endpoint == __value.endpoint
                and self.description == __value.description
                and self.item_type == __value.item_type
                and self.length == __value.length
                and self.reproductions == __value.reproductions
                and self.album_item == __value.album_item
                and self.artist_items == __value.artist_items
            )
        else:
            return False

    def __hash__(self):
        return hash(
            (
                self.name,
                self.thumbnail_url,
                self.endpoint,
                self.description,
                self.item_type,
                self.reproductions,
                self.length,
                self.album_item,
                self.artist_items,
            )
        )


class ProfileItem(Item):
    def __init__(self, handle: Optional[str] = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.handle = handle
        self.item_type = ItemType.PROFILE

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + f", handle={self.handle}" "}"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, ProfileItem):
            return (
                self.name == __value.name
                and self.thumbnail_url == __value.thumbnail_url
                and self.endpoint == __value.endpoint
                and self.description == __value.description
                and self.item_type == __value.item_type
                and self.handle == __value.handle
            )
        else:
            return False

    def __hash__(self):
        return hash(
            (
                self.name,
                self.thumbnail_url,
                self.endpoint,
                self.description,
                self.item_type,
                self.handle,
            )
        )


class PodcastItem(Item):
    def __init__(
        self,
        length: Optional[time] = None,
        artist_items: List[ArtistItem] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        if artist_items is None:
            artist_items = []
        self.length = length
        self.artist_items = artist_items
        self.item_type = ItemType.PODCAST

    def __repr__(self):
        return (
            super().__repr__()[:-1] + f", length={self.length}"
            f", artist_items={self.artist_items}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, PodcastItem):
            return (
                self.name == __value.name
                and self.thumbnail_url == __value.thumbnail_url
                and self.endpoint == __value.endpoint
                and self.description == __value.description
                and self.item_type == __value.item_type
                and self.length == __value.length
                and self.artist_items == __value.artist_items
            )
        else:
            return False

    def __hash__(self):
        return hash(
            (
                self.name,
                self.thumbnail_url,
                self.endpoint,
                self.description,
                self.item_type,
                self.length,
                self.artist_items,
            )
        )


class EpisodeItem(Item):
    def __init__(
        self,
        publication_date: Optional[date] = None,
        length: Optional[time] = None,
        artist_items: List[ArtistItem] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        if artist_items is None:
            artist_items = []
        self.length = length
        self.publication_date = publication_date
        self.artist_items = artist_items
        self.item_type = ItemType.PODCAST

    def __repr__(self):
        return (
            super().__repr__()[:-1] + f", publication_date={self.publication_date}"
            f", length={self.length}"
            f", artist_items={self.artist_items}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, EpisodeItem):
            return (
                self.name == __value.name
                and self.thumbnail_url == __value.thumbnail_url
                and self.endpoint == __value.endpoint
                and self.description == __value.description
                and self.item_type == __value.item_type
                and self.length == __value.length
                and self.artist_items == __value.artist_items
                and self.publication_date == __value.publication_date
            )
        else:
            return False

    def __hash__(self):
        return hash(
            (
                self.name,
                self.thumbnail_url,
                self.endpoint,
                self.description,
                self.item_type,
                self.length,
                self.artist_items,
                self.publication_date,
            )
        )

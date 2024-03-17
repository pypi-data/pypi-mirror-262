from .note import Note
from .user import User, UserLite, avatarDecorations
from .drive import DriveFile, df_property, DriveFolder

from ..exception import ParseError


async def parse_note(json: dict):
    try:
        deco = []
        files = []
        if json["user"]["avatarDecorations"]:
            for d in json["user"]["avatarDecorations"]:
                deco.append(
                    avatarDecorations(
                        d["id"],
                        d["url"],
                        d["angle"],
                        d["flipH"]
                    )
                )
        if json["files"]:
            for file in json["files"]:
                files.append(
                    DriveFile(
                        file["id"],
                        file["createdAt"],
                        file["name"],
                        file["type"],
                        file["md5"],
                        file["size"],
                        file["isSensitive"],
                        file["blurhash"],
                        df_property(
                            file["properties"]["width"],
                            file["properties"]["height"],
                            file["properties"]["orientation"],
                            file["properties"]["avgColor"],
                        ),
                        file["url"],
                        file["thunbnailUrl"],
                        file["comment"],
                        file["folderid"],
                        DriveFolder(
                            file["folder"]["id"],
                            file["folder"]["createdAt"],
                            file["folder"]["name"],
                            file["folder"]["parentId"],
                            file["folder"]["foldersCount"],
                            file["folder"]["filesCount"],
                            file["folder"]["parent"],
                        ),
                        file["userId"],
                        User(
                            file["user"]["id"],
                            file["user"]["createdAt"],
                            file["user"]["username"],
                            file["user"]["host"],
                            file["user"]["name"],
                            file["user"]["avatarUrl"],
                            file["user"]["avatarBlurhash"],
                            file["user"]["avatarDecorations"],
                            file["user"]["isAdmin"],
                            file["user"]["isModerator"],
                            file["user"]["isBot"],
                            file["user"]["isCat"],
                            file["user"]["onlineStatus"]
                        )
                    )
                )
        object = Note(
            json["id"],
            json["createdAt"],
            json["deletedAt"],
            json["text"],
            json["cw"],
            json["userId"],
            UserLite(
                json["user"]["id"],
                json["user"]["username"],
                json["user"]["host"],
                json["user"]["name"],
                json["user"]["avatarUrl"],
                json["user"]["avatarBlurhash"],
                json["user"]["avatarDecorations"],
                json["user"]["isAdmin"],
                json["user"]["isModerator"],
                json["user"]["isBot"],
                json["user"]["isCat"],
                json["user"]["onlineStatus"]
            ),
            json["replyId"],
            json["renoteId"],
            json["reply"],
            json["renote"],
            json["isHidden"],
            json["visibility"],
            json["mentions"],
            json["visibleUserIds"],
            json["fileIds"],
            files,
            json["tags"],
            json["poll"],
            json["channelId"],
            json["channel"],
            json["localOnly"],
            json["reactionAcceptance"],
            json["reactions"],
            json["renoteCount"],
            json["replyesCount"],
            json["uri"],
            json["url"],
            json["reactionAndUserPairCache"],
            json["myReaction"]
        )
        return object
    except KeyError as e:
        ParseError(e)
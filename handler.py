from methods import *


def handler(recv: dict) -> dict:
    sent = {}
    request = recv["type"]

    if request == "login":
        msg, result = login(recv["userid"], recv["psd"])
    elif request == "userinfo":
        msg, result = userInfo(recv["userid"])
    elif request == "showposts":
        msg, result = showPosts()
    elif request == "postinfo":
        msg, result = postinfo(recv["postid"])
    elif request == "newuser":
        msg, result = newUser(recv["name"], recv["psd"])
    elif request == "banuser":
        msg, result = banUser(recv["userid"], recv["banuid"])
    elif request == "setadmin":
        msg, result = setAdmin(recv["userid"], recv["setuid"])
    elif request == "newpost":
        msg, result = newPost(
            recv["userid"], recv["headline"], recv["contains"])
    elif request == "delpost":
        msg, result = delPost(recv["userid"], recv["delpid"])
    elif request == "newcomment":
        msg, result = newComment(
            recv["userid"], recv["postid"], recv["comment"])
    elif request == "delcomment":
        msg, result = delComment(
            recv["userid"], recv["postid"], recv["delflr"])

    sent.update(msg)
    sent["result"] = result
    return sent

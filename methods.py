from connect import *
from datetime import datetime


USERKEY = ("userid", "name", "isadmin", "isbanned")
POSTKEY = ("postid", "userid", "headline", "contains",
           "crtime", "floors", "isdelete", "deleterid", "deltime")
COMTKEY = ("postid", "floor","userid", "comment",
           "crtime", "isdelete", "deleterid", "deltime")

SEARCHLINE = "select {} from {} where {}"
INSERTLINE = "insert into {} values {}"
UPDATELINE = "update {} set {}"
NEXTVALINE = "select nextval('{}')"

LOGINLINE = "userid={} and psd='{}'"
NEWUSERLINE = "({},'{}','{}')"
BANUSERLINE = "isbanned=true where userid={}"
NEWPOSTLINE = "({},{},'{}','{}','{}')"
DELPOSTLINE = "isdelete=true,deleterid={},deltime='{}' where postid={}"
NEWCOMTLINE = "({},{},{},'{}','{}')"
DELCOMTLINE = "isdelete=true,deleterid={},deltime='{}' where postid={} and floor={}"

MSGKEY = ("status", "message")


@decrator
def userInfo(userid: int, curs):

    curs.execute(SEARCHLINE.format(
        ",".join(USERKEY), "forum.users", "userid={}".format(userid)))
    result = curs.fetchall()

    if len(result):
        msg = dict(zip(MSGKEY, ("SUCCESS", "查找成功!")))
        result = dict(zip(USERKEY, result[0]))
    else:
        msg = dict(zip(MSGKEY, ("ERROR", "查无此人!")))
        result = None
    return msg, result, curs


@decrator
def login(userid: int, psd: str, curs):
    curs.execute(SEARCHLINE.format(",".join(USERKEY),
                 "forum.users", LOGINLINE.format(userid, psd)))
    result = curs.fetchall()

    if len(result):
        msg = dict(zip(MSGKEY, ("SUCCESS", "登录成功!")))
        result = dict(zip(USERKEY, result[0]))
    else:
        msg = dict(zip(MSGKEY, ("ERROR", "登录失败:请检查账号或密码")))
        result = None

    return msg, result, curs


@decrator
def newUser(name: str, psd: str, curs):
    try:
        curs.execute(NEXTVALINE.format("forum.uid"))
        userid = (curs.fetchall())[0][0]
        curs.execute(INSERTLINE.format(
            'forum.users (userid,name,psd)', NEWUSERLINE.format(userid, name, psd)))
        curs.execute(SEARCHLINE.format(
            ",".join(USERKEY), "forum.users", "userid={}".format(userid)))
        result = curs.fetchall()

        msg = dict(zip(MSGKEY, ("SUCCESS", "账号创建成功!")))
        result = dict(zip(USERKEY, result[0]))
        print(msg, result)
        return msg, result, curs

    except:
        msg = dict(zip(MSGKEY, ("ERROR", "用户名已被使用!")))
        result = None
        print(msg, result)
        return msg, result, curs


@decrator
def banUser(myid: int, banid: int, curs):
    curs.execute(SEARCHLINE.format("isadmin,isbanned",
                                   "forum.users", "userid ={}".format(myid)))
    isadmin, isbanned = curs.fetchall()[0]
    if isadmin and not isbanned:
        curs.execute(UPDATELINE.format(
            "forum.users", BANUSERLINE.format(banid)))
        msg = dict(zip(MSGKEY, ("SUCCESS", "封禁成功!")))
        result = None
        return msg, result, curs
    else:
        msg = dict(zip(MSGKEY, ("ERROR", "封禁失败:权限不足或您已被封禁!")))
        result = None
        return msg, result, curs


@decrator
def setAdmin(myid: int, setid: int, curs):

    curs.execute(SEARCHLINE.format("isadmin,isbanned",
                 "forum.users", "userid ={}".format(myid)))
    isadmin, isbanned = curs.fetchall()[0]
    if isadmin and not isbanned:
        curs.execute(UPDATELINE.format(
            "forum.users", "isadmin=true where userid={}".format(setid)))
        msg = dict(zip(MSGKEY, ("SUCCESS", "赋权成功!")))
        result = None
        return msg, result, curs
    else:
        msg = dict(zip(MSGKEY, ("ERROR", "赋权失败:权限不足或您已被封禁!")))
        result = None
        return msg, result, curs


@decrator
def newPost(userid: int, headline: str, contains: str, curs):
    curs.execute(SEARCHLINE.format("isbanned",
                 "forum.users", "userid ={}".format(userid)))
    isbanned = (curs.fetchall())[0][0]
    if not isbanned:
        curs.execute(NEXTVALINE.format("forum.pid"))
        postid = (curs.fetchall())[0][0]

        curs.execute(INSERTLINE.format('forum.posts', NEWPOSTLINE.format(
            postid, userid, headline, contains, datetime.now())))

        msg = dict(zip(MSGKEY, ("SUCCESS", "发帖成功!")))
        result = None
        return msg, result, curs
    else:
        msg = dict(zip(MSGKEY, ("ERROR", "发帖失败:账号被封禁!")))
        result = None
        return msg, result, curs


@decrator
def delPost(userid: int, postid: int, curs):
    curs.execute(SEARCHLINE.format("isadmin,isbanned",
                 "forum.users", "userid ={}".format(userid)))
    isadmin, isbanned = curs.fetchall()[0]
    curs.execute(SEARCHLINE.format("*",
                 "forum.posts", "userid ={} and postid={}".format(userid, postid)))
    iscruser = bool(len(curs.fetchall()))

    if (iscruser or isadmin) and not isbanned:
        curs.execute(UPDATELINE.format(
            "forum.posts", DELPOSTLINE.format(userid, datetime.now(), postid)))
        msg = dict(zip(MSGKEY, ("SUCCESS", "删帖成功!")))
        result = None
        return msg, result, curs
    else:
        msg = dict(zip(MSGKEY, ("ERROR", "删帖失败:权限不足或您已被封禁!")))
        result = None
        return msg, result, curs


@decrator
def newComment(userid: int, postid: int, comment: str, curs):
    curs.execute(SEARCHLINE.format("isbanned",
                 "forum.users", "userid ={}".format(userid)))
    isbanned = (curs.fetchall())[0][0]
    if not isbanned:
        curs.execute(SEARCHLINE.format(
            "floors", "forum.posts", "postid={}".format(postid)))
        floor = curs.fetchall()[0][0]+1
        curs.execute(UPDATELINE.format(
            "forum.posts", "floors={} where postid={}".format(floor, postid)))
        curs.execute(INSERTLINE.format("forum.comments",
                                       NEWCOMTLINE.format(postid, floor, userid, comment, datetime.now())))
        msg = dict(zip(MSGKEY, ("SUCCESS", "评论成功!")))
        result = None
        return msg, result, curs
    else:
        msg = dict(zip(MSGKEY, ("ERROR", "评论失败:您已被封禁!")))
        result = None
        return msg, result, curs


@decrator
def delComment(userid: int, postid: int, floor: int, curs):
    curs.execute(SEARCHLINE.format("isadmin,isbanned",
                 "forum.users", "userid ={}".format(userid)))
    isadmin, isbanned = curs.fetchall()[0]

    curs.execute(SEARCHLINE.format("*",
                 "forum.posts", "userid={} and postid={}".format(userid, postid)))
    iscruser = bool(len(curs.fetchall()))

    curs.execute(SEARCHLINE.format("*",
                 "forum.comments", "userid={} and postid={} and floor={}".format(userid, postid, floor)))
    iscomter = bool(len(curs.fetchall()))

    if (iscomter or iscruser or isadmin) and not isbanned:
        curs.execute(UPDATELINE.format(
            "forum.comments", DELCOMTLINE.format(userid, datetime.now(), postid, floor)))
        msg = dict(zip(MSGKEY, ("SUCCESS", "删评成功!")))
        result = None
        return msg, result, curs
    else:
        msg = dict(zip(MSGKEY, ("ERROR", "删评失败:权限不足或您已被封禁!")))
        result = None
        return msg, result, curs


@decrator
def showPosts(curs):
    curs.execute(SEARCHLINE.format("*", "forum.posts",
                 "isdelete=false order by crtime desc"))
    posts = curs.fetchall()

    result = []
    for post in posts:
        result.append(dict(zip(POSTKEY, post)))

    result={"postlist":result}
    msg = dict(zip(MSGKEY, ("SUCCESS", "查询成功!")))
    return msg, result, curs


@decrator
def postinfo(postid: int, curs):
    curs.execute(SEARCHLINE.format("*", "forum.posts",
                 "postid={} and isdelete=false".format(postid)))
    post = curs.fetchall()

    if bool(len(post)):
        result=dict(zip(POSTKEY,post[0]))
        curs.execute(SEARCHLINE.format("*", "forum.comments",
                 "postid={} and isdelete=false order by floor".format(postid)))
        comments = curs.fetchall()
        comtlist=[]
        for comt in comments:
            comtlist.append(dict(zip(COMTKEY,comt)))
        msg = dict(zip(MSGKEY, ("SUCCESS", "查询成功!")))
        result.update({"comments":comtlist})
    else:
        msg = dict(zip(MSGKEY, ("ERROR", "帖子不存在或已删除!")))
        result=None
    return msg,result,curs

postinfo(3)
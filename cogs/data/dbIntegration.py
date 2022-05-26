from operator import truediv
import os
from unittest import result
from bson.objectid import ObjectId

from pymongo import MongoClient
from random import randrange

from pytest import console_main

from cogs.data.console import *

cluster = MongoClient(os.getenv("DATABASE_CLIENT_URL"))
db = cluster["BabuPsaja"]
Console_Sepator()
Console("MongoDB", "Connected!")
Console_Sepator()

#Birthday =>
birthdays = db["Birthdays"]

#Prefix =>
prefix_collection = db["prefixes"]
Console("MongoDB", "PrefixDB loaded")

#Truth or dare =>
truthordare = db["Data"]

truthordare_DataDB =  truthordare.find_one({"_id": ObjectId(str("6239a1be57cf9e4a1d86029c"))})

DareData = truthordare_DataDB["dare"]
TruthData = truthordare_DataDB["truth"]

#Truth or dare remove empty line =>
def stringToList(string):
    listRes = list(string.split("\n"))
    return listRes
    
DareData_list = stringToList(DareData)
TruthData_list = stringToList(TruthData)
Console("MongoDB", "TruthOrDareDB loaded")

#Ben =>
BenData = db["Discord Data"]
Console("MongoDB", "BenDB loaded")

#Voter =>
VoterData = db["poll data"]
Console("MongoDB", "VoteDB loaded")

#Voice =>
VoiceData = db["voice data"]
Console("MongoDB", "VoiceDB Loaded")

#Prune =>
MemberData = db["Member Data"]
Console("MongoDB", "MemberDB Loaded")

Console_Sepator()

"""https://github.com/0xcabrex/Rexbot/blob/c25707f31a5e895123333823def11aed565cd0fa/cogs/usefullTools/dbIntegration.py#L94"""
"""Prefixes Event"""
def fetch_prefix(guild_id):

	results = None
	results = prefix_collection.find_one({"guild_id": int(guild_id)})
	return results


def insert_prefix(guild_id, prefix):

    prefix_check = None
    prefix_check = prefix_collection.find_one({"guild_id": int(guild_id)})

    if prefix_check is None:
        results = prefix_collection.insert_one({"guild_id": int(guild_id), "prefix": str(prefix)})
        Console("DB", "PrefixDB new prefix")
    else:
        results = prefix_collection.update_one({"guild_id": int(guild_id)}, {"$set": {"prefix": str(prefix)}})
        Console("DB", "PrefixDB new prefix")


def del_prefix(guild_id):

	results = prefix_collection.delete_one({"guild_id": guild_id})

def get_prefix(client, message):
    try:
        return fetch_prefix(message.guild.id)["prefix"]
    except:
        prefix = ">"
        return prefix

"""Ben"""
def Ben_FindGuild(The_ID : str):
    return BenData.find_one({"guildid": The_ID})

def Ben_Exist(Search : str, The_ID : str):
    if BenData.count_documents({Search: The_ID}) != 0:
        return True
    else:
        return False

def Ben_Delete(any):
    BenData.delete_one(any) 

def Ben_InsertData(custom_id : int, channel_id, member_id, guild_id):
    post = {"_id": custom_id, "channelid": channel_id, "memberid": member_id, "guildid": guild_id}
    BenData.insert_one(post)
    Console("DB", "Ben data inserted " + str(custom_id))


"""Truth Or Dare"""
def CheckData(custom_id : str):
    if truthordare.count_documents({ 'secondid': custom_id }, limit = 1) != 0:
        return True
    else:
        return False

def DeleteDataTOD(custom_id : str):
    if truthordare.count_documents({ 'secondid': custom_id }, limit = 1) != 0:
        post = {'secondid': custom_id}
        truthordare.delete_one(post)
        Console("DB", "Truth or dare data deleted " + custom_id)
        return True
    else:
        return False


#Dare
def InsertData_Dare(custom_id : str, value : str):
    post = {"secondid": custom_id, "dare": value}
    truthordare.insert_one(post)
    Console("DB", "Dare data inserted " + custom_id)

def GetData_Dare():

    return DareData

def UpdateData_Dare(id : str, value : str):
    post = {'_id': ObjectId(str(id))},  {'$set': {"dare": f"{value}"}}
    truthordare.update_one(post)
    Console("DB", "Dare data updated")

def UpdateAndDelete_Dare(id : str, custom_id : str):
    if CheckData(custom_id=custom_id) == True:
        SecondDataDB =  truthordare.find_one({"secondid": custom_id})
        NewData = SecondDataDB["dare"]
        truthordare.update_one({"_id": ObjectId(str(id))},  {'$set': {"dare": DareData + "\n" + NewData}})
        truthordare.delete_one({'secondid': custom_id}) 
        Console("DB", "Added new dare data")


#Truth
def InsertData_Truth(custom_id : str, value : str):
    post = {"secondid": custom_id, "truth": value}
    truthordare.insert_one(post)
    Console("DB", "Truth data inserted " + custom_id)

def GetData_Truth():

    return TruthData

def UpdateData_Truth(id : str, value : str):
    post = {'_id': ObjectId(str(id))},  {'$set': {"truth": f"{value}"}}
    truthordare.update_one(post)
    Console("DB", "Truth data updated")

def UpdateAndDelete_Truth(id : str, custom_id : str):
    if CheckData(custom_id=custom_id) == True:
        SecondDataDB =  truthordare.find_one({"secondid": custom_id})
        NewData = SecondDataDB["truth"]
        truthordare.update_one({"_id": ObjectId(str(id))},  {'$set': {"truth": TruthData + "\n" + NewData}})
        truthordare.delete_one({'secondid': custom_id}) 
        Console("DB", "Added new truth data")

"""Advance Voice Channel"""
def InsertUserVoiceData(voice_owner : int, channel_id : int):
    VoiceData.insert_one({"voice_owner": voice_owner, "channel_id": channel_id})
    Console("DB", "Added new voice data")

def DeleteUserVoiceData(voice_owner : int):
    VoiceData.delete_one({'voice_owner': voice_owner}) 
    Console("DB", "Delete voice data")

def GetUserVoice(voice_owner : int):
    if VoiceData.count_documents({"voice_owner": voice_owner}) != 0:
        return True
    else:
        return False

def GetUserVoice_ChannelID(voice_owner : int):
    VoiceOwner = VoiceData.find_one({"voice_owner": int(voice_owner)})
    Data = VoiceOwner["channel_id"]
    return Data

"""Psaja Prune Member"""
def GetExpired():
    MemberData_ = MemberData.find_one({"_id", ObjectId(str("625fe1d61aadaa322c371b64"))})
    Data = MemberData_["Expired"]
    return Data

def GetMemberList():
    MemberData_ = MemberData.find_one({"_id", ObjectId(str("625fe1d61aadaa322c371b64"))})
    Data = MemberData_["MemberList"]
    return Data

def GetMember():
    MemberData_ = MemberData.find_one({"_id", ObjectId(str("625fe1d61aadaa322c371b64"))})
    Data = MemberData_["MemberList"]
    list = stringToList(str(Data))
    return list

def IfMemberExist(Member : str):
    MemberList = GetMember()
    if Member in MemberList:
        return True
    else:
        return False

def CloseSession():
    MemberData.update_one({"_id": ObjectId(str("625fe1d61aadaa322c371b64"))},  {'$set': {"Expired": "True"}})

def OpenSession():
    MemberData.update_one({"_id": ObjectId(str("625fe1d61aadaa322c371b64"))},  {'$set': {"Expired": "False"}})

def InsertMember(Member : str):
    MemberData_ = MemberData.find_one({"_id", ObjectId(str("625fe1d61aadaa322c371b64"))})
    Data = MemberData_["MemberList"]
    MemberData.update_one({"_id": ObjectId(str("625fe1d61aadaa322c371b64"))},  {'$set': {"MemberList": Data + "\n" + Member}})
    Console("DB", "Inserted Member Data")

def ClearMemberDB(Member : str):
    MemberData_ = MemberData.find_one({"_id", ObjectId(str("625fe1d61aadaa322c371b64"))})
    Data = MemberData_["MemberList"]
    MemberData.update_one({"_id": ObjectId(str("625fe1d61aadaa322c371b64"))},  {'$set': {"MemberList": "None"}})
    Console("DB", "Member Data Cleared")

        
        
import os
import re
import secrets
import shutil
# subprocess is only used with a fixed argument list and no shell
import subprocess  # nosec B404
import tempfile

POINTS = {"win" : 3, "draw": 1, "loss": 0}
REFEREE_PASSWORD = os.environ.get("REFEREE_PASSWORD")
teams = {}
matches = []


def addTeam(teamName, players=[]):
    teams[teamName] = {"played": 0, "won": 0, "drawn": 0, "lost": 0,
                       "gf": 0, "ga": 0, "players": players}


def matchResult(homeGoals, awayGoals):
    if homeGoals > awayGoals:
        return "home"
    elif homeGoals < awayGoals:
        return "away"
    else:
        return "draw"


def recordMatch(home, away, homeGoals, awayGoals):
    result = matchResult(homeGoals, awayGoals)
    sides = ((home, homeGoals, awayGoals), (away, awayGoals, homeGoals))
    for team, scored, conceded in sides:
        teams[team]["played"] += 1
        teams[team]["gf"] += scored
        teams[team]["ga"] += conceded
    if result == "draw":
        teams[home]["drawn"] += 1
        teams[away]["drawn"] += 1
    else:
        winner, loser = (home, away) if result == "home" else (away, home)
        teams[winner]["won"] += 1
        teams[loser]["lost"] += 1
    matches.append((home, away, homeGoals, awayGoals))


def points(teamName):
    stats = teams[teamName]
    return stats["won"] * POINTS["win"] + stats["drawn"] * POINTS["draw"]


def goalDifference(teamName):
    return teams[teamName]["gf"] - teams[teamName]["ga"]


def leagueTable():
    return sorted(teams, key=lambda t: (points(t), goalDifference(t)),
                  reverse=True)


def isTopTwo(teamName):
    table = leagueTable()
    return teamName == table[0] or teamName == table[1]

def tossCoin():
    return secrets.choice(["Heads", "Tails"])


def tableFilePath():
    # Helper kept for the lab: not called by the demo
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    return path


def publishTable(server):
    # Helper kept for the lab: not called by the demo
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.@_-]*", server):
        raise ValueError("Invalid server name: " + repr(server))
    scp = shutil.which("scp")
    if scp is None:
        raise FileNotFoundError("scp is not installed")
    # No shell is used and the server name is validated above
    subprocess.run([scp, "--", "table.json", server + ":/var/www/"],
                   check=True)  # nosec B603


def main():
    for name in ["Royal Strikers", "City Rovers", "Lake United"]:
        addTeam(name)
    addTeam("Hill Warriors")
    print("Toss:", tossCoin())
    recordMatch("Royal Strikers", "City Rovers", 2,1)
    recordMatch("Lake United", "Hill Warriors", 0, 0)
    recordMatch("City Rovers", "Lake United", 3, 2)
    recordMatch("Hill Warriors", "Royal Strikers", 1, 1)
    print("Pos Team Played Won Drawn Lost Pts")
    for pos, name in enumerate(leagueTable(), 1):
        stats = teams[name]
        print(pos, name, stats["played"], stats["won"], stats["drawn"],
              stats["lost"], points(name)) # one row per team
    print("Is City Rovers in the top two?", isTopTwo("City Rovers"))
    print("Matches played:", len(matches))


main()
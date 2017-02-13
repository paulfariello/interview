#!/usr/bin/env python3
#
# Copyright (c) 2016 Paul Fariello <paul@fariello.eu>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""A rest API providing access to Interview management

Request to this REST API must be done with Content-Type: application/json as
all sent data is expected to be well formed json.
"""

import sys
import argparse
import bottle
import json
import datetime
from peewee import fn

import uniqid
import model

ISO8601_FMT = "%Y-%m-%d"
STATIC_ROOT = None

app = application = bottle.Bottle()

def strpdate(date):
    return datetime.datetime.strptime(date[:10], ISO8601_FMT).date()

@app.get("/")
@app.get(r"/<path:re:.*\.(html|js|css|woff2|woff|ttf|jpg)>")
def static(path=None):
    """Unsafe method used only for dev"""
    if path is None:
        path = "index.html"
    return bottle.static_file(path, root=STATIC_ROOT)

@app.get(r"/api/status")
def create_account():
    """Get server status

    Exemple:
    curl -X GET -H "Content-Type:application/json" http://localhost:8001/api/status
    """
    return json.dumps({'status': 'OK'})

@app.post(r"/api/applicant/")
def create_applicant():
    """Create a new applicant

    Exemple:
    curl -X POST -H "Content-Type:application/json" -d '{"name": "Paul Fariello"}' http://localhost:8001/api/applicant/
    """
    uid = uniqid.generate()
    name = bottle.request.json['name']
    applicant = model.Applicant.create(uid=uid, name=name)
    return json.dumps(applicant.json, indent="  ")


@app.get(r"/api/applicant/<applicant_id:re:[a-zA-Z0-9_=-]+>")
def get_applicant(applicant_id):
    """Get applicant description

    Exemple:
    curl -X GET -H "Content-Type:application/json" http://localhost:8001/api/applicant/PoP93u9ktzqIP5-cJx1D9D
    """
    try:
        uid = uniqid.decode(applicant_id)
        applicant = model.Applicant.get(model.Applicant.uid == uid)
    except model.Applicant.DoesNotExist as e:
        bottle.response.status = 404
        return {"error": "Applicant %s not found" % applicant_id}
    return json.dumps(applicant.json, indent="  ")


@app.post(r"/api/interview/")
def create_interview():
    """Create a new interview

    Exemple:
    curl -X POST -H "Content-Type:application/json" -d '{"applicant": "PoP93u9ktzqIP5-cJx1D9D"}' http://localhost:8001/api/interview/
    """
    try:
        uid = uniqid.decode(bottle.request.json['applicant'])
        applicant = model.Applicant.get(model.Applicant.uid == uid)
        uid = uniqid.generate()
        token = uniqid.generate()
        interview = model.Interview.create(uid=uid, token=token, applicant=applicant)
    except model.Applicant.DoesNotExist as e:
        bottle.response.status = 404
        return {"error": "Applicant %s not found" % applicant_id}
    return json.dumps(interview.json, indent="  ")

@app.get(r"/api/interview/")
def get_interview():
    """Get all interview

    Exemple:
    curl -X GET -H "Content-Type:application/json" http://localhost:8001/api/interview/
    """
    interviews = model.Interview.select().execute()
    return json.dumps([interview.json for interview in interviews], indent="  ")


@app.get(r"/api/interview/<interview_id:re:[a-zA-Z0-9_=-]+>")
def get_interview(interview_id):
    """Get interview description

    Exemple:
    curl -X GET -H "Content-Type:application/json" http://localhost:8001/api/interview/3sb8p5VpnYL-DFm-RbI0lC
    """
    try:
        uid = uniqid.decode(interview_id)
        interview = model.Interview.get(model.Interview.uid == uid)
    except model.Interview.DoesNotExist as e:
        bottle.response.status = 404
        return {"error": "Interview %s not found" % interview_id}
    return json.dumps(interview.json, indent="  ")


@app.get(r"/api/interview/<interview_token:re:[a-zA-Z0-9_=-]+>/pass")
def pass_interview(interview_token):
    """Get interview description for an applicant to pass

    Exemple:
    curl -X GET -H "Content-Type:application/json" http://localhost:8001/api/interview/r6_yv14TrKYbNxMNhnMYyB/pass
    """
    try:
        token = uniqid.decode(interview_token)
        interview = model.Interview.get(model.Interview.token == token)
    except model.Interview.DoesNotExist as e:
        bottle.response.status = 404
        return {"error": "Interview %s not found" % interview_id}
    pass_json = interview.json
    del pass_json['uid']
    return json.dumps(pass_json, indent="  ")


@app.post(r"/api/exercice/")
def create_exercice():
    """Create a new exercice

    Exemple:
    curl -X POST -H "Content-Type:application/json" -d '{"question": "La grande question sur la vie, l'"'"'univers et le reste", "tags": ["fun"]}' http://localhost:8001/api/exercice/
    """
    uid = uniqid.generate()
    question = bottle.request.json['question']
    exercice = model.Exercice.create(uid=uid, question=question)
    for tag in bottle.request.json['tags']:
        tag, created = model.Tag.get_or_create(name=tag)
        rel = model.ExerciceTagRel.create(exercice=exercice, tag=tag)
    return json.dumps(exercice.json, indent="  ")


@app.get(r"/api/exercice/")
def get_exercice():
    """Create a new exercice

    Exemple:
    curl -X GET -H "Content-Type:application/json" http://localhost:8001/api/exercice/
    """
    exercices = model.Exercice.select().execute()
    return json.dumps([exercice.json for exercice in exercices], indent="  ")


@app.put(r"/api/interview/<interview_id:re:[a-zA-Z0-9_=-]+>/exercices/<index:int>")
def attach_exercice(interview_id, index):
    """Attach an exercice at a given position in an interview

    Exemple:
    curl -X PUT -H "Content-Type:application/json" -d '{"exercice": "4pofihCDVrJwPNGsuz9LvD"} http://localhost:8001/api/interview/PoP93u9ktzqIP5-cJx1D9D/exercices/1
    """
    try:
        uid = uniqid.decode(interview_id)
        interview = model.Interview.get(model.Interview.uid == uid)
        uid = uniqid.decode(bottle.request.json['exercice'])
        exercice = model.Exercice.get(model.Exercice.uid == uid)
        exercice = model.ExerciceAttribution.create(interview=interview, exercice=exercice, index=index)
    except model.Interview.DoesNotExist as e:
        bottle.response.status = 404
        return {"error": "Interview %s not found" % interview_id}
    except model.Exercice.DoesNotExist as e:
        bottle.response.status = 404
        return {"error": "Exercice %s not found" % exercice_id}
    return json.dumps(exercice.json, indent="  ")


@app.post(r"/api/interview/<interview_id:re:[a-zA-Z0-9_=-]+>/exercices/")
def attach_exercice(interview_id):
    """Attach an exercice at the end of an interview

    Exemple:
    curl -X POST -H "Content-Type:application/json" -d '{"exercice": "4pofihCDVrJwPNGsuz9LvD"} http://localhost:8001/api/interview/PoP93u9ktzqIP5-cJx1D9D/exercices/
    """
    try:
        uid = uniqid.decode(interview_id)
        # TODO commit
        interview = model.Interview.get(model.Interview.uid == uid)
        max_index = model.ExerciceAttribution.select().where(model.ExerciceAttribution.interview == interview)\
                       .aggregate(fn.Max(model.ExerciceAttribution.index))
        max_index = max_index or 0
        uid = uniqid.decode(bottle.request.json['exercice'])
        exercice = model.Exercice.get(model.Exercice.uid == uid)
        exercice = model.ExerciceAttribution.create(interview=interview, exercice=exercice, index=max_index+1)
    except model.Interview.DoesNotExist as e:
        bottle.response.status = 404
        return {"error": "Interview %s not found" % interview_id}
    except model.Exercice.DoesNotExist as e:
        bottle.response.status = 404
        return {"error": "Exercice %s not found" % exercice_id}
    return json.dumps(exercice.json, indent="  ")


@app.delete(r"/api/interview/<interview_id:re:[a-zA-Z0-9_=-]+>/exercices/<exercice_id:re:[a-zA-Z0-9_=-]+>")
def detach_exercice(interview_id, exercice_id):
    """Detach an exercice from an interview

    Exemple:
    curl -X DELETE -H "Content-Type:application/json" http://localhost:8001/api/interview/PoP93u9ktzqIP5-cJx1D9D/exercices/4pofihCDVrJwPNGsuz9LvD
    """
    try:
        uid = uniqid.decode(interview_id)
        interview = model.Interview.get(model.Interview.uid == uid)
        uid = uniqid.decode(exercice_id)
        exercice = model.Exercice.get(model.Exercice.uid == uid)
        where = (model.ExerciceAttribution.interview == interview) \
                & (model.ExerciceAttribution.exercice == exercice)
        model.ExerciceAttribution.delete().where(where).execute()
    except model.Interview.DoesNotExist as e:
        bottle.response.status = 404
        return {"error": "Interview %s not found" % interview_id}
    except model.Exercice.DoesNotExist as e:
        bottle.response.status = 404
        return {"error": "Exercice %s not found" % exercice_id}

@app.route(r"/api/interview/<interview_token_or_id:re:[a-zA-Z0-9_=-]+>/exercices/<index:int>", method='GET')
def get_answer(interview_token_or_id, index):
    """Get answer of a given exercice

    Exemple:
    curl -X GET -H "Content-Type:application/json" http://localhost:8001/api/interview/PoP93u9ktzqIP5-cJx1D9D/exercices/1
    """
    try:
        uid = uniqid.decode(interview_token_or_id)
        where = (model.Interview.uid == uid) | (model.Interview.token == uid)
        interview = model.Interview.get(where)
        where = (model.ExerciceAttribution.interview == interview) \
                & (model.ExerciceAttribution.index == index)
        exercice = model.ExerciceAttribution.get(where)
        try:
            answers = model.Answer.select().where(model.Answer.exercice==exercice)\
                               .order_by(model.Answer.date).execute()
        except model.Answer.DoesNotExist as e:
            answer = None
    except model.Interview.DoesNotExist as e:
        bottle.response.status = 404
        return {"error": "Interview %s not found" % interview_token_or_id}
    except model.ExerciceAttribution.DoesNotExist as e:
        bottle.response.status = 404
        return {"error": "Exercice %s not found" % index}
    dump = exercice.json
    if answers:
        dump['history'] = [answer.json for answer in answers]
    else:
        dump['history'] = {}
    return json.dumps(dump, indent="  ")

@app.route(r"/api/interview/<interview_token:re:[a-zA-Z0-9_=-]+>/exercices/<exercice_id:re:[a-zA-Z0-9_=-]+>", method='PUT')
def answer_exercice(interview_token, exercice_id):
    """Answer a given exercice

    Exemple:
    curl -X PUT -H "Content-Type:application/json" -d '{"answer": "42"} http://localhost:8001/api/interview/PoP93u9ktzqIP5-cJx1D9D/exercices/4pofihCDVrJwPNGsuz9LvD
    """
    try:
        uid = uniqid.decode(interview_token)
        interview = model.Interview.get(model.Interview.token == uid)
        uid = uniqid.decode(exercice_id)
        exercice = model.Exercice.get(model.Exercice.uid == uid)
        answer = bottle.request.json['answer']
        where = (model.ExerciceAttribution.interview == interview) \
                & (model.ExerciceAttribution.exercice == exercice)
        exercice = model.ExerciceAttribution.get(where)
        answer = model.Answer.create(exercice=exercice, answer=answer)
    except model.Interview.DoesNotExist as e:
        bottle.response.status = 404
        return {"error": "Interview %s not found" % interview_id}
    except model.Exercice.DoesNotExist as e:
        bottle.response.status = 404
        return {"error": "Exercice %s not found" % exercice_id}
    except model.ExerciceAttribution.DoesNotExist as e:
        bottle.response.status = 404
        return {"error": "ExerciceAttribution not found"}
    return json.dumps(answer.json, indent="  ")


def main():
    """Start server"""
    parser = argparse.ArgumentParser(description="Interview")
    parser.add_argument("-l", "--listen", dest="host", default="0.0.0.0", help="IP address to bind to")
    parser.add_argument("-p", "--port", dest="port", default=os.environ.get('PORT', 8001), type=int,
                        help="Port to listen to")
    parser.add_argument("--db", dest="db", default=os.environ.get('POSTGRESQL_ADDON_URI', "sqlite:///interview.db"),
                        help="Database scheme to connect to")
    parser.add_argument("--static", dest="static", default=None, type=str, help="Path to static files")
    parser.add_argument("--server", dest="server", default='auto', type=str, help="Bottle server type")
    parser.add_argument("--init", dest="init", action="store_true", help="Initialize database")
    args, remaining = parser.parse_known_args()
    sys.argv = [sys.executable] + remaining

    model.connect(args.db)
    if args.init:
        model.create_tables()

    global STATIC_ROOT
    STATIC_ROOT = args.static

    app.run(server=args.server, host=args.host, port=args.port)

if __name__ == "__main__":
    main()

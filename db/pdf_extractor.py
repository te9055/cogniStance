#extracting text from PDFs
from tika import parser
import os
from pathlib import Path


#cleaning documents
import pandas as pd
from os import listdir
from datetime import datetime
import click

#db connection
from db.db_config import get_db

conn, cursor = get_db()

def skip_empty_lines(f):
    # Skip any empty lines
    for l in f:
        if l.strip():
            return l.strip()


def skip_irrelevant(f):
    # Skip the white spaces and "Page X of Y"
    res = skip_empty_lines(f)

    while res.startswith("Page"):
        res = skip_empty_lines(f)

    return res

def read_skipping_header(f, top_title=None):
    # This reads the text skipping the "Page X of Y" and the next empty line.
    # If top_title is given and matches the line after that, that is also skipped and the next empty line

    l = next(f, None)
    while l is not None:
        l = l.strip()

        if l.startswith("Page "):
            l = next(f, None)
            while l and l.strip():
                l = next(f, None)

            if top_title:

                l = next(f, None)
                while l and l.strip():
                    l = next(f, None)

            continue

        if l is not None:
            yield l
        else:
            break

        l = next(f, None)

def parse_document(filename):
    res = {
        "filename": filename
    }

    try:
        with open(filename, 'r') as f:
            res["initial_title"] = skip_irrelevant(f)


            f = read_skipping_header(f, res["initial_title"])

            # There always seems to be a header (which may be multiple lines, possibly including empty lines),
            # a source (which seems to consistently be one line) and a publication date (also one line).

            # I choose to read all three of them together, as the date seems to be the only concrete end point.
            res["pub_date"] = None
            tmp = []
            while res["pub_date"] is None:
                l = skip_empty_lines(f)

                # Eventually, we should find the date (this should only happen after header and source have been found)
                try:
                    # June 6, 2024 Thursday
                    res["pub_date"] = datetime.strptime(
                        ' '.join(l.split(' ')[:3]),
                        # Format is inconsistent, with some cases having full time. I only get up to day and discard the rest
                        "%B %d, %Y"
                    ).strftime("%Y-%m-%d")

                    # If the above succeeds, we should have found both the header and source
                    assert len(tmp) >= 2, "We have not found enough lines for both header and source"

                    res["header"] = ''.join(tmp[:-1])
                    res["source"] = tmp[-1]
                except ValueError:
                    tmp.append(l)

            l = skip_empty_lines(f)
            res["copyright"] = ""
            while not l.startswith("Length: "):
                res["copyright"] += l + '\n'

                l = skip_empty_lines(f)

            res["other_top"] = ""
            while l != "Body":
                if l:
                    if ": " in l:
                        k, v = l.split(": ")

                        res[k] = v
                    else:
                        res["other_top"] += l + '\n'

                l = skip_empty_lines(f)

            body = []
            for l in f:
                if l == "Classification":
                    break

                body.append(l)

            res["body"] = "\n".join(body)

            res["other_classification"] = ""
            l = skip_empty_lines(f)
            while l != "End of Document":
                if l:
                    if ": " in l:
                        k, v = l.split(": ")

                        if k == "Load-Date":
                            v = datetime.strptime(
                                v,
                                "%B %d, %Y"
                            ).strftime("%Y-%m-%d")

                        res[k] = v
                    else:
                        res["other_classification"] += l + '\n'

                l = skip_empty_lines(f)
    except Exception as e:
        print(e)
        print(filename)

    return res

def getinputfiles(dir):
    files = os.listdir(dir)
    return files

def savetotxt(file, content):
    file1 = open(file, "w")
    file1.write(content)
    file1.close()

def simpleextraction(f):
    outdir = 'out/'
    raw = parser.from_file('files/' + f)
    location = os.path.dirname(os.path.abspath('files/' + f))
    rawcontent = raw['content']
    outname = f.split(".")
    title = outname[0]
    file = outdir + outname[0] + '.txt'
    savetotxt(file, rawcontent)
    parsedtxt = parse_document(file)

    pubdate = parsedtxt['pub_date']
    pubyear = parsedtxt['pub_date'].split('-')[0].strip()
    websource = parsedtxt['source']
    cleanedcontent = parsedtxt['body']
    loaddate = parsedtxt['Load-Date']
    res = {
        "title": title,
        "location": location,
        "pubyear": pubyear,
        "pubdate": pubdate,
        "websource": websource,
        "loaddate": loaddate,
        "cleanedcontent": cleanedcontent,
        "rawcontent": rawcontent
    }
    return res

def savetodb(res):
    cursor.execute("INSERT INTO news VALUES ('"+str(res['id'])+"','"+res['title']+"','"+res['location']+"','"+res['pubyear']+"','"+res['pubdate']+"','"+res['websource']+"','"+res['loaddate']+"','"+res['cleanedcontent']+"');")
    conn.commit()
    conn.close()

def main():
    inputdir = 'files'
    dsstore = Path("files/.DS_Store")
    if dsstore.exists():
        os.remove("files/.DS_Store")

    files = getinputfiles(inputdir)

    counter = 0
    for f in files:
        res = simpleextraction(f)
        res['id'] = counter
        savetodb(res)
        counter = counter + 1



if __name__ == '__main__':
    main()
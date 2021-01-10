import io
import json
import os
import uuid


def getId():
    return str(uuid.uuid4())

def openfile(name):

    f = io.open(name, "r", encoding="utf-8")
    t = f.read()
    f.close()
    return t

def writefile(name, content):
    f = io.open(name, "w", encoding="utf-8")
    f.write(content)
    f.close()
    return f



def aggregate(result,setting, data, isContent):

    if(setting == ""):
        return result

    isList = False

    if(setting == "image_slide"):
        isList = True
        data = data.split(" ")
        while '' in data:
            data.remove('')

    if(not isList):
        data = data.strip()


    if(not isContent):
        result[setting] = data
    else:
        result["content"].append({"type": setting, "value": data})

    return result


def processElement(element):

    rows = element.split("\n")

    rows_no_emptys = []
    for row in rows:
        if(len(row) > 0):
            rows_no_emptys.append(row)

    if(len(rows_no_emptys) == 0):
        return None

    setting = ""
    data = ""

    result = {}
    result["content"] = []
    isContent = False

    for row in rows_no_emptys:

        if(row == "Category:"):
            result = aggregate(result,setting, data, isContent)
            isContent = False
            data = ""
            setting = "type"
        elif(row == "Title:"):
            result = aggregate(result,setting, data, isContent)
            isContent = False
            data = ""
            setting = "title"
        elif(row == "MainImage:"):
            result = aggregate(result,setting, data, isContent)
            isContent = False
            data = ""
            setting = "preview_image"
        elif(row == "EndPreview:"):
            result = aggregate(result,setting, data, isContent)
            isContent = True
            data = ""
            setting = "end_preview"
        elif(row == "Text:"):
            result = aggregate(result,setting, data, isContent)
            isContent = True
            data = ""
            setting = "text"
        elif(row == "Collegamento:"):
            result = aggregate(result,setting, data, isContent)
            isContent = True
            data = ""
            setting = "link_ref"
        elif(row == "Video:"):
            result = aggregate(result,setting, data, isContent)
            isContent = True
            data = ""
            setting = "video"
        elif(row == "SlideShow:"):
            result = aggregate(result,setting, data, isContent)
            isContent = True
            data = ""
            setting = "image_slide"
        else:
            data += row + " "

    result = aggregate(result,setting, data, isContent)

    result["id"] = getId()

    return result


def injectJsons(elements):

    javascript = ""
    for element in elements:

        el = processElement(element)

        if(el != None):
            javascript += json.dumps(el, indent=4, ensure_ascii=False) + ",\n"

    javascript = javascript[:-2]

    return javascript

def workOnFile(filePath):
    t = openfile(filePath)
    elements = t.split("END_ARTICLE")
    return injectJsons(elements)


def main():

    javascript = "\n//Document autogenerated\n"
    javascript += "var DocuVale = [\n"

    for f in os.listdir("./ArticoliVale"):
        print("Processing: ", f)
        javascript += workOnFile("./ArticoliVale/" + f) + ",\n"

    javascript = javascript[:-2]
    javascript += "];\n"

    writefile("./Logics/autogenWorks.js", javascript)

    print("autogenWorks created!")

if(__name__ == "__main__"):
    main()

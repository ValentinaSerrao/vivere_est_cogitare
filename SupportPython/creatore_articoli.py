import io
import json
import os




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

    if(setting == "image_slide" or setting == "image_inline"):
        isList = True
        data = data.split("\n")
        while '' in data:
            data.remove('')

    if(not isList):
        data = data.strip()


    if(not isContent):
        result[setting] = data
    else:
        result["content"].append({"type": setting, "value": data})

    return result


def processElement(element, fname):

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
        elif(row == "Date:"):
            result = aggregate(result,setting, data, isContent)
            isContent = False
            data = ""
            setting = "date"
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
        elif(row == "Separator:"):
            result = aggregate(result,setting, data, isContent)
            isContent = True
            data = ""
            setting = "separator"
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
        elif(row == "ImageInline:"):
            result = aggregate(result,setting, data, isContent)
            isContent = True
            data = ""
            setting = "image_inline"
        elif(row == "ImageTextOnRight:"):
            result = aggregate(result,setting, data, isContent)
            isContent = True
            data = ""
            setting = "image_text_on_rigth"
        elif(row == "LinkInline:"):
            result = aggregate(result,setting, data, isContent)
            isContent = True
            data = ""
            setting = "link_inline"
        elif(row == "SlideShow:"):
            result = aggregate(result,setting, data, isContent)
            isContent = True
            data = ""
            setting = "image_slide"
        else:
            data += row + "\n"

    result = aggregate(result,setting, data, isContent)

    result["id"] = fname

    return result


def injectJsons(elements, fname):

    javascript = ""
    for element in elements:

        el = processElement(element, fname)

        if(el != None):
            javascript += json.dumps(el, indent=4, ensure_ascii=False) + ",\n"

    javascript = javascript[:-2]

    return javascript

def workOnFile(filePath, fname):
    t = openfile(filePath)
    elements = t.split("END_ARTICLE")
    return injectJsons(elements, fname)


def main():

    javascript = "\n//Document autogenerated\n"
    javascript += "var DocuVale = [\n"

    for f in os.listdir("./ArticoliVale"):
        print("Processing: ", f)
        javascript += workOnFile("./ArticoliVale/" + f, f.split(".")[0]) + ",\n"

    javascript = javascript[:-2]
    javascript += "];\n"

    writefile("./Logics/autogenWorks.js", javascript)

    print("autogenWorks created!")

if(__name__ == "__main__"):
    main()

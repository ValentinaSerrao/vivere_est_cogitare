
var initedWorks = false;

var ValeProgetti = {
  "Blogs": [],
  "Gregorios": []
};

function initAllWorks(){

  if(initedWorks){
    return;
  }

  for(let i = 0; i < DocuVale.length; i++){

    let docu = DocuVale[i];
    let type = docu["type"];
    let img = docu["preview_image"];
    let title = docu["title"];
    let id = docu["id"];
    let content = processContent(docu["content"]);

    let processed = {
      "title": title,
      "id": id,
      "preview_image": img,
      "content": content
    }

    if(type == "Blog"){
      processed["main_title"] = "Articoli";
      ValeProgetti["Blogs"].push(processed);
    }
    if(type == "Gregorio"){
      processed["main_title"] = "Progetti SSML Gregorio VII";
      ValeProgetti["Gregorios"].push(processed);
    }
  }

  initedWorks = true;

}

function processContent(content) {

  let html = "<div>";

  for(let i = 0; i < content.length; i++){

    let el = content[i];

    let type = el["type"];
    let val = el["value"];

    if(type == "end_preview"){
      html += "<div class=\"article_text_preview_change\">" + val + "</div><div style=\"display:none;\">END_PREVIEW</div>";
    }
    if(type == "text"){
      html += "<div class=\"article_text\">" + val + "</div>";
    }
    if(type == "video"){
      html += "<iframe class=\"video_iframe\" src=\""+val+"\"></iframe>";
    }
    if(type == "link_ref"){
      html += buildLink(val);
    }
    if(type == "image_slide"){
      html += buildImageSliderHtml(val);
    }
  }

  html += "</div>";

  return html;

}

function buildLink(val) {

  let spl = val.split(" ");
  let spl_no_link = [];
  for(let i = 2; i < spl.length; i++){
    spl_no_link.push(spl[i]);
  }

  let link_ref = spl[0];
  let link_near_label = spl[1] + " ";
  let text = spl_no_link.join(" ");


  let link = "<div class=\"article_content_link_label\">"+link_near_label+"<a style=\"color: #2d6d7b;\" href=\""+link_ref+"\" target=\"_blank\">"+text+"</a></div>";
  return link;
}

function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

function buildImageSliderHtml(list_imgs) {

  let slide_show_rand_id = uuidv4();

  let wrap = "<div id=\""+slide_show_rand_id+"\" class=\"slide_show_wrap\"><div class=\"slide_show_wrap_images\" name=\"slide_shower\"><div class=\"left_slide_button\" onclick=\"slideshowMoveLeft('"+slide_show_rand_id+"');\">‹</div>INNER_IMAGES<div class=\"right_slide_button\" onclick=\"slideshowMoveRight('"+slide_show_rand_id+"');\">›</div></div><div class=\"slide_show_buttons_wrapper\">INNER_BUTTONS</div></div>";

  let slides = "";
  let buttons = "";
  for(let i = 0; i < list_imgs.length; i++){

    let class_for_img = "image_slide_show";
    let class_for_button = "slide_show_button_selected";
    if(i > 0){
      class_for_img = "image_slide_show_hidden";
      class_for_button = "slide_show_button";
    }

    slides += "<img class=\""+class_for_img+"\" src=\""+list_imgs[i]+"\" class=\"slide_show_img\">\n";
    buttons += "<div class=\""+class_for_button+"\" onclick=slideShowChange('"+i.toString() + "___" +slide_show_rand_id+"');></div>";
  }

  wrap = wrap.replace("INNER_IMAGES", slides).replace("INNER_BUTTONS",buttons);

  return wrap;
}

function initSlideShowerEventListeners() {
  let sliders = document.getElementsByName("slide_shower");
  for(let i = 0; i < sliders.length; i++){
    sliders[i].addEventListener('mouseenter', showSlidersArrows);
    sliders[i].addEventListener('mouseleave', hideSlidersArrows);
  }
}

function showSlidersArrows(){
  let src = event.srcElement;
  let targ = src.children;
  for(let i = 0; i < targ.length; i++){
      if(targ[i].nodeName == "DIV"){
        targ[i].style.display = "inline-block";
      }
  }
}

function hideSlidersArrows(){
  let src = event.srcElement;
  let targ = src.children;
  for(let i = 0; i < targ.length; i++){
      if(targ[i].nodeName == "DIV"){
        targ[i].style.display = "none";
      }
  }
}

function getSliderSelectedIndexAndMazSize(id) {
  let slider = document.getElementById(id);
  let slider_images_and_divs_wrap = slider.children[0];
  let slider_images_and_divs = slider_images_and_divs_wrap.children;
  let index = -1;
  for(let i = 0; i < slider_images_and_divs.length; i++){
      if(slider_images_and_divs[i].className == "image_slide_show"){
        index = i;
      }
  }
  return [index-1, slider_images_and_divs.length-2];
}

function slideshowMoveLeft(id) {
  let index_and_max = getSliderSelectedIndexAndMazSize(id);
  let index = index_and_max[0];
  if(index>0){
    index--;
    slideShowChange(index.toString() + "___" + id);
  }
}

function slideshowMoveRight(id) {
  let index_and_max = getSliderSelectedIndexAndMazSize(id);
  let index = index_and_max[0];
  let max = index_and_max[1];
  if(index<max-1){
    index++;
    slideShowChange(index.toString() + "___" + id);
  }
}


function slideShowChange(index___id) {

  let spl = index___id.split("___");
  let index = spl[0];
  let id = spl[1];

  let slider = document.getElementById(id);

  let slider_images_and_divs_wrap = slider.children[0];
  let slider_buttons_wrap = slider.children[1];

  let slider_images_and_divs = slider_images_and_divs_wrap.children;
  let buttons = slider_buttons_wrap.children;
  let images = [];
  for(let i = 0; i < slider_images_and_divs.length; i++){
      if(slider_images_and_divs[i].nodeName == "IMG"){
        images.push(slider_images_and_divs[i]);
      }
  }

  for(let i = 0; i < images.length; i++){
    images[i].className = "image_slide_show_hidden";
  }
  images[index].className = "image_slide_show";

  for(let i = 0; i < buttons.length; i++){
    buttons[i].className = "slide_show_button";
  }
  buttons[index].className = "slide_show_button_selected";

}

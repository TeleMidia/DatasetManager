/*
Copyright (C) 2019  Telemidia/PUC-Rio <http://www.telemidia.puc-rio.br/>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


function doKeyDown(e) {
  if (annotator == null)
    return;

   var key_code = e.keyCode;

   if (key_code == 45 || key_code == 100){
    annotator.remove_current_bb();
    annotator.update_json_document()
   }
  
}

function change_canvas_scale(signal, canvas_id){
    if (annotator == null)
      return;

      var canvas =  document.getElementById(canvas_id)

      var new_width = canvas.width + signal;

      dims = annotator.get_max_min_dims()

      if (new_width > dims[0])
        new_width = dims[0]
      else if (new_width < dims[1])
        new_width = dims[1] 

      var new_height = parseInt((canvas.height*new_width)/canvas.width)

      canvas.width  = new_width;
      canvas.height = new_height;

    /*
    var cur_scale = annotator.get_scale();

    cur_scale += signal;

    if (cur_scale < 50)
      cur_scale = 50;
    else if(cur_scale > 100)
      cur_scale = 100;
    */

    annotator.set_scale(100);

}

function mouse_down_event(event){
  if (annotator == null)
    return;
  annotator.mouse_down(event.offsetX, event.offsetY);
}

function mouse_up_event(event){
  if (annotator == null)
    return;
  annotator.mouse_up(event.offsetX, event.offsetY);
}

function mouse_drag_event(event){
  if (annotator == null)
    return;
  annotator.mouse_drag(event.offsetX, event.offsetY);
}

function select_label_event(label_index, label_str){

  if (annotator == null)
    return;   

  annotator.set_label(label_index-1);
}

function upload_json_dodument(form){
  if (annotator == null)
    return;

    var dataset_id = annotator.get_dataset();
    var cur_media_id = annotator.get_cur_media_id();

    form.action = "/set_annotation/"+dataset_id+"/"+cur_media_id;
    form.querySelector("#json_document").value =  annotator.export_json();

    form.submit();

}

class BoundingBox {
    constructor(id_i, label_id_i, x_i, y_i) {
      this.x = x_i;
      this.y = y_i;
      this.w = 10;
      this.h = 10;
      this.id = id_i;
      this.label_id = label_id_i;
      var rgb = getColorByInt(this.label_id);
      this.color = "rgb("+rgb[0]+","+rgb[1]+","+rgb[2]+")";
      this.line_wdth = 4;
      
      //control
      this.is_seleced = true;
      this.select_mode = 4;
      this.trace_size = 5;

      //console.log("bb", this.id, "has been created.");
    }
    get_data(){
      return [this.label_id, this.x, this.y, this.w, this.h];
    }
    set_origin(x, y){
      this.x = x;
      this.y = y;
    }
    set_dims(width, height){
      this.w = width;
      this.h = height;
    }
    change_label(label_id_i){
      this.label_id = label_id_i;
      var rgb = getColorByInt(this.label_id);
      this.color = "rgb("+rgb[0]+","+rgb[1]+","+rgb[2]+")";
    }

    is_selected(){
      return this.is_seleced;
    }
    tick(){
      //console.log(this.id);
      if (this.is_seleced == false)
        return;

      if (this.trace_size >= 5)
        this.trace_size = 3;
      else
        this.trace_size = 5;
    }
    unselect(){
      this.is_seleced = false;

      if (this.w < 0) {
        this.x = this.x + this.w;
        this.w = this.w*-1;
      }

      if (this.h < 0){
        this.y = this.y + this.h;
        this.h = this.h*-1
      }

     // console.log(this.x, this.y, this.w, this.h); 
    }
    select(mouse_x, mouse_y){
      if (mouse_x >= this.x && mouse_x <= (this.x+this.w)){
        if (mouse_y >= this.y && mouse_y <= (this.y+this.h)){
          this.is_seleced = true;
          this.select_mode = 0;

          var dif_x = Math.abs(mouse_x - this.x);
          var dif_y = Math.abs(mouse_y - this.y);
          if (dif_x <= 10 && dif_y <= 10)
            this.select_mode = 1;

          var dif_x = Math.abs(mouse_x - (this.x+this.w));
          var dif_y = Math.abs(mouse_y - this.y);
          if (dif_x <= 10 && dif_y <= 10)
            this.select_mode = 2;

          var dif_x = Math.abs(mouse_x - this.x);
          var dif_y = Math.abs(mouse_y - (this.y+this.h));
          if (dif_x <= 10 && dif_y <= 10)
            this.select_mode = 3;

          var dif_x = Math.abs(mouse_x - (this.x+this.w));
          var dif_y = Math.abs(mouse_y - (this.y+this.h));
          if (dif_x <= 10 && dif_y <= 10)
            this.select_mode = 4;

          return true;
        }
      }
    }

    edit(w_i, h_i){

      if (this.select_mode == 0){
        this.x = w_i - (this.w/2);
        this.y = h_i - (this.h/2);
      }
      else if (this.select_mode == 1){
        var dif1 = (this.y-h_i);
        var dif2 = (this.x-w_i);
        this.y = h_i;
        this.h = this.h + dif1;
        this.x = w_i;
        this.w = this.w + dif2;
      }
      else if (this.select_mode == 2){
        this.w = w_i - this.x;
        var dif = (this.y-h_i);
        this.y = h_i;
        this.h = this.h + dif;
      }
      else if (this.select_mode == 3){
        this.h = h_i - this.y;
        var dif = (this.x-w_i);
        this.x = w_i;
        this.w = this.w + dif;
      }
      else if (this.select_mode == 4){
        this.w = w_i - this.x;
        this.h = h_i - this.y;
      }
      
  
      //console.log(this.x, this.y, this.w, this.h);  
    }
    draw(ctx) {

      ctx.strokeStyle = this.color;
      ctx.fillStyle =  this.color;
      ctx.globalAlpha = 0.2;
      ctx.fillRect(this.x, this.y, this.w, this.h);
      ctx.globalAlpha = 1.0;

      /*
      ctx.font = 'normal 12px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillStyle = 'white';
      ctx.fillText("loading media ...", parseInt(this.x + (this.w/2)), parseInt(this.y + (this.h/2))); 
      */

      ctx.beginPath();
      ctx.lineWidth = this.line_wdth;
      if (this.is_seleced == true)
        ctx.setLineDash([5, this.trace_size]);
      ctx.rect(this.x, this.y, this.w, this.h);
      ctx.stroke();
      
      //ctx.font = "normal 12px Arial";
      //ctx.fillStyle = "red";
      //ctx.textAlign = "center";
      //ctx.strokeText("BB", this.x+(this.w/2), this.y+20);

      if (this.is_seleced == false)
        return;

      ctx.setLineDash([]);  

      var offset_x = 0;
      var offset_y = 0;

      //square 1
      ctx.beginPath();
      ctx.lineWidth = this.line_wdth;
      ctx.strokeStyle = this.color;
      if (this.w < 0)
        offset_x = -10
      if (this.h < 0)
        offset_y = -10
      ctx.rect(this.x+offset_x, this.y+offset_y, 10, 10);
      ctx.stroke();

      offset_x = 0;
      offset_y = 0;

      //square 2
      ctx.beginPath();
      ctx.lineWidth = this.line_wdth;
      ctx.strokeStyle = this.color;
      if (this.w < 0)
        offset_x = 10;
      if (this.h < 0)
        offset_y = -10;
      ctx.rect(this.x+offset_x+(this.w-10), this.y+offset_y, 10, 10);
      ctx.stroke();

      //square 3
      ctx.beginPath();
      ctx.lineWidth = this.line_wdth;
      ctx.strokeStyle = this.color;
      if (this.w < 0)
        offset_x = -10;
      if (this.h < 0)
        offset_y = 10;
      ctx.rect(this.x+offset_x, this.y+offset_y+(this.h-10), 10, 10);
      ctx.stroke();

      //square 4
      ctx.beginPath();
      ctx.lineWidth = this.line_wdth;
      ctx.strokeStyle = this.color;
      if (this.w < 0)
        offset_x = 10;
      if (this.h < 0)
        offset_y = 10;
      ctx.rect(this.x+offset_x+(this.w-10), this.y+offset_y+(this.h-10), 10, 10);
      ctx.stroke();

    }
}

class Annotator {
    constructor(canvas_id, submitForm_id) {
      this.sismo_image = null;
      this.flag_loaded_img = false;
      this.canvas_id = canvas_id;
      this.ctx = document.getElementById(canvas_id);
      this.submitForm = document.getElementById(submitForm_id);
      this.dataset_id = null;
      this.current_media_id = null;
   

      this.canvas_width = this.ctx.offsetWidth;
      this.canvas_height = this.ctx.offsetHeight;


      this.ctx.addEventListener("mousedown", mouse_down_event, false);
      this.ctx.addEventListener("mouseup", mouse_up_event, false);
      this.ctx.addEventListener("mousemove", mouse_drag_event, false);
     
      
      if (this.ctx.getContext) {
        this.ctx = this.ctx.getContext('2d');
      }
      
      this.boundingBoxes = new Array();
      this.labelsList = new Array();

      //controls
      this.mouse_is_down = false; 
      this.acctime = 0
      this.startTime = new Date();
      this.currentLabel = 0
      this.max_width = null;
      this.min_width = null;
      this.img_loaded = false;
    }

    get_bbQtd(){
      return this.boundingBoxes.length;
    }

    add_bb(bb){
      this.boundingBoxes.push(bb);
    }
    get_width_height(){
      return [this.canvas_width, this.canvas_height];
    }
  
    set_max_min_dims(max_width, min_width){
      this.max_width = max_width;
      this.min_width = min_width;
    }

    get_max_min_dims(){
      return [this.max_width, this.min_width]
    }

    update_canvas_size_label(){
      
      var label = document.getElementById("scaleLabel"); 
      label.innerHTML = this.canvas_width+" x "+this.canvas_height+" (w x h)";
    }

    set_dimsBasedOnImageSize(img_w, img_h){

      var canvas = document.getElementById(this.canvas_id); 

      canvas.height = parseInt((canvas.width*img_h)/img_w);

      this.canvas_width = canvas.offsetWidth;
      this.canvas_height = canvas.offsetHeight;

      this.update_canvas_size_label();
    }

    set_scale(scale){

      var canvas = document.getElementById(this.canvas_id); 
      
        for (var bs = 0; bs < this.boundingBoxes.length; bs++) {

          var data = this.boundingBoxes[bs].get_data();
        
       
          var x = (data[1]/this.canvas_width);
          var y = (data[2]/this.canvas_height);
          var w = (data[3]/this.canvas_width);
          var h = (data[4]/this.canvas_height);

          this.boundingBoxes[bs].set_origin(parseInt(x*canvas.offsetWidth), parseInt(y*canvas.offsetHeight));
          this.boundingBoxes[bs].set_dims(parseInt(w*canvas.offsetWidth), parseInt(h*canvas.offsetHeight));

          this.update_canvas_size_label();
        }
       
      this.canvas_width = canvas.offsetWidth;
      this.canvas_height = canvas.offsetHeight;

      console.log("dims changed to:", this.canvas_width, this.canvas_height);
    }

    set_dataset(dataset_id){
      this.dataset_id = dataset_id;
    }

    get_dataset(){
      return this.dataset_id;
    }

    set_cur_media_id(media_id){
      this.current_media_id = media_id;
    }

    get_cur_media_id(){
      return this.current_media_id;
    }

    remove_current_bb(){

      if (this.img_loaded == false)
        return;

      var act_box_index = -1;

      for (var s_i = 0; s_i < this.boundingBoxes.length; s_i++) {
        if (this.boundingBoxes[s_i].is_selected() == true)
           act_box_index = s_i;
      } 

      if (act_box_index < 0)
        return;
       
     this.boundingBoxes.splice(act_box_index, 1);

    }

    set_label(label_index){

      if (label_index >= this.labelsList.length)
        return;
      
      this.currentLabel = label_index;  

     //console.log("going to change", label_index);   
     var act_box_index = -1;

     for (var s_i = 0; s_i < this.boundingBoxes.length; s_i++) {
       if (this.boundingBoxes[s_i].is_selected() == true)
          act_box_index = s_i;
     } 

     //console.log("changed", act_box_index);

      if (act_box_index < 0)
        return;

      this.boundingBoxes[act_box_index].change_label(label_index);
     
      this.update_json_document();
        
    }
    add_labels(labels_i){
      for (var j=0; j < labels_i.length; j++){
        this.labelsList.push(labels_i[j]);
      }

      //console.log("labels added", this.labelsList.length);
    }
    set_loaded_flag(value){
      this.img_loaded = value;
    }

    load_image(img_src){
      this.img_loaded = false;
      this.sismo_image = new Image();
      this.sismo_image.onload = function() {
        annotator.set_dimsBasedOnImageSize(this.width, this.height);
        annotator.set_loaded_flag(true);
      };
      this.sismo_image.src = img_src;

      //console.log("loading media", img_src)
    }

    clear_boundingboxes(){
      while (this.boundingBoxes.length) {
        this.boundingBoxes.pop();
      }
    }

    update_json_document(){
      upload_json_dodument(this.submitForm);
    }

    mouse_up(mouse_x, mouse_y){
      if (this.img_loaded == false)
        return;

      this.mouse_is_down = false;
      //console.log("mouse_up", mouse_x, mouse_y); 
      
      this.update_json_document();
    }

    mouse_down(mouse_x, mouse_y){
      if (this.img_loaded == false)
        return;


      this.mouse_is_down = true;

      var select_one = false;

      for (var i = 0; i < this.boundingBoxes.length; i++) {
        this.boundingBoxes[i].unselect();
      } 

      for (var i = 0; i < this.boundingBoxes.length; i++) {
        if(this.boundingBoxes[i].select(mouse_x, mouse_y)){
          return;
        }
      }

      var bb_id = this.boundingBoxes.length; 
      var bb = new BoundingBox(bb_id, this.currentLabel, mouse_x, mouse_y);
      this.boundingBoxes.push(bb);
      //console.log("mouse_up", mouse_x, mouse_y);  
    }

    mouse_drag(mouse_x, mouse_y){
      //console.log(this.mouse_down)
      if (this.img_loaded == false)
        return;
      
      if (this.mouse_is_down == true){
        //console.log("mouse_drag", mouse_x, mouse_y);
        for (var i = 0; i < this.boundingBoxes.length; i++) {
          if (this.boundingBoxes[i].is_selected() == true){
            this.boundingBoxes[i].edit(mouse_x, mouse_y);
            break;
          }
        } 
      }
      return this.something_changed;
    }

    draw() {

      if (this.img_loaded == false){
        this.ctx.fillStyle = "black";
        this.ctx.fillRect(0, 0, this.canvas_width, this.canvas_height);
        this.ctx.font = 'normal bold 20px sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.fillStyle = 'white';
        this.ctx.fillText("loading media ...", parseInt(this.canvas_width/2), parseInt(this.canvas_height/2) ); 
        return;
      }


      var curtime = new Date();
      this.acctime = this.acctime + (curtime - this.startTime); 
      this.startTime = new Date();  
      
      if (this.sismo_image != null){
        this.ctx.drawImage(this.sismo_image, 0, 0, this.canvas_width, this.canvas_height);
      }

      for (var i = 0; i < this.boundingBoxes.length; i++) {
        this.boundingBoxes[i].draw(this.ctx);
        if (this.acctime >= 500 && this.boundingBoxes[i].is_selected()== true){
          this.boundingBoxes[i].tick();
          this.acctime = 0;
        }
      } 

    }

    export_json() {
      var json = "{ \"boundinboxes\": [";
      
      for (var js = 0; js < this.boundingBoxes.length; js++) {

        var data = this.boundingBoxes[js].get_data();
        
        //console.log("saving");
        //console.log("canvas dim:", this.canvas_width, this.canvas_height);
        //console.log("ant", data);

        data[1] = (data[1]/this.canvas_width);
        data[2] = (data[2]/this.canvas_height);
        data[3] = (data[3]/this.canvas_width);
        data[4] = (data[4]/this.canvas_height);

        //console.log("pos", data);
        

        json = json + "{\"tag\": "+data[0]+", \"x\": "+data[1]+", \"y\": "+data[2]+", \"w\": "+data[3]+", \"h\": "+data[4]+"}";
        if (js < (this.boundingBoxes.length-1)){
          json = json + ",";
        }
      }

      json = json + "] }";

      return json;
    }

    request_annotation() {
      $.get("/get_annotation/"+this.dataset_id+"/"+this.current_media_id, function(req_data, status){
          if (status == "success"){
              var json_data = JSON.parse(req_data);
             
              for (var ba = 0; ba < json_data.boundinboxes.length; ba++){
                  var bb = json_data.boundinboxes[ba];
                  var label = bb.tag; 

                  var canvas_dim = annotator.get_width_height();

                  var pos_x = bb.x*canvas_dim[0]; 
                  var pos_y = bb.y*canvas_dim[1]; 
                  var pos_w = bb.w*canvas_dim[0]; 
                  var pos_h = bb.h*canvas_dim[1];

                  //console.log("loading");
                  //console.log("canvas dim:", canvas_dim);
                  //console.log("ant", bb);
                  //console.log("pos", label, pos_x, pos_y, pos_w, pos_h);

                  var bb_id = annotator.get_bbQtd(); 
                  var new_bb = new BoundingBox(bb_id, label, pos_x, pos_y);
                  new_bb.set_dims(pos_w, pos_h);
                  new_bb.unselect();
                  annotator.add_bb(new_bb);

                  
              }

          }
      });
    }
}

var annotator = new Annotator('sismo_canvas','formUploadJson');
webpackJsonp([4],{VvQJ:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var s=a("Xxa5"),i=a.n(s),n=a("exGp"),r=a.n(n),c=a("gyMJ"),o=a("L/O1"),l={data:function(){return{total:0,page_size:20,data_list:[],loading:!0,id_list:[],username:Object(o.b)("username")}},components:{},computed:{get_page:function(){var t=this.$route.params.page;return t?parseInt(t):1},director:function(){return this.$route.params.bid}},created:function(){this.getData()},methods:{getData:function(){var t=this;return r()(i.a.mark(function e(){var a,s;return i.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return a={page:t.get_page,page_size:t.page_size,data:{director:t.director},total:t.total},e.next=3,Object(c.j)(a);case 3:s=e.sent,t.total=s.total,console.log(s),t.total>0&&(t.data_list=s.data),t.loading=!1;case 8:case"end":return e.stop()}},e,t)}))()},delData:function(){var t=this;return r()(i.a.mark(function e(){var a,s;return i.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:if(console.log(Array(t.id_list)),0!==(a=t.id_list.length)){e.next=5;break}return t.$Message.warning("please select movie."),e.abrupt("return");case 5:return s={id_list:Array(t.id_list),username:t.username},e.next=8,Object(c.f)(s);case 8:1===e.sent.state?(t.total-=a,t.$Message.success("删除成功")):t.$Message.warning("删除失败"),t.id_list=[],t.getData();case 12:case"end":return e.stop()}},e,t)}))()},del:function(t,e){var a=this;return r()(i.a.mark(function s(){return i.a.wrap(function(s){for(;;)switch(s.prev=s.next){case 0:return s.next=2,Object(c.f)({id:e,username:a.username});case 2:1===s.sent.state?(a.data_list.splice(t,1),a.total-=1,a.$Message.success("删除成功")):a.$Message.warning("删除失败");case 4:case"end":return s.stop()}},s,a)}))()},addMoviecol:function(t){var e=this;return r()(i.a.mark(function a(){var s;return i.a.wrap(function(a){for(;;)switch(a.prev=a.next){case 0:return a.next=2,Object(c.c)({id:t});case 2:0===(s=a.sent).state?e.$Message.warning("用户未登录"):1===s.state?e.$Message.success("收藏成功"):e.$Message.success("收藏失败");case 4:case"end":return a.stop()}},a,e)}))()},show:function(t){var e=t.split(" ")[0];this.$router.push({path:"/"+e})},seturl:function(t){return t=t.split(" ")[0],this.server_ip+"/image/movie/"+t+"/"+t+".jpg?"+Math.random()},settitle:function(t){return t=t.split(" ").slice(1).join(" ")},settext:function(t){return t=t.split(" ")[0]},changeState:function(){var t=this;return r()(i.a.mark(function e(){return i.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,Object(c.d)({id_list:t.id_list});case 2:1===e.sent.state?(t.$Message.success("设置成功"),t.id_list=[]):t.$Message.warning("设置失败");case 4:case"end":return e.stop()}},e,t)}))()},changePage:function(t){this.id_list=[],this.page=t,this.$router.push("/director/"+this.director+"/"+t)},changePagesize:function(t){this.page_size=t,console.log("page_size:",this.page_size),this.getData()}},watch:{$route:function(t,e){this.getData()}}},u={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"main"},[t.loading?a("Spin",{attrs:{size:"large",fix:""}}):t._e(),t._v(" "),a("div",{staticClass:"index-body"},[a("div",{staticStyle:{"text-align":"left",margin:"auto"}},[a("CheckboxGroup",{model:{value:t.id_list,callback:function(e){t.id_list=e},expression:"id_list"}},t._l(t.data_list,function(e,s){return a("div",{staticClass:"index-item"},[a("div",{staticClass:"item-img",on:{click:function(a){t.show(e.title)}}},[a("div",{staticStyle:{width:"315.3px",height:"212.3px"}},[a("img",{staticStyle:{height:"212.3px",width:"315.3px"},attrs:{src:t.seturl(e.title),alt:e.title}})])]),t._v(" "),a("div",{staticClass:"item-text"},[a("div",{staticClass:"item-text-title"},[t._v(t._s(e.info))]),t._v(" "),a("div",{staticClass:"item-text-name"},["xiaoxin"===t.username?a("Checkbox",{attrs:{label:e.id}},[a("span",{staticStyle:{margin:"0",padding:"0"}})]):t._e(),t._v("\n              "+t._s(t.settext(e.title))+"/"+t._s(t.$formatDate(e.release_time))+"\n              "),a("Button",{attrs:{size:"small"},on:{click:function(a){t.addMoviecol(e.id)}}},[t._v("收藏")]),t._v(" "),"xiaoxin"===t.username?a("Button",{attrs:{size:"small"},on:{click:function(a){t.del(s,e.id)}}},[t._v("删除")]):t._e()],1)])])}))],1),t._v(" "),"xiaoxin"===t.username?a("div",{staticStyle:{position:"fixed",top:"5px",left:"524px",width:"110px","z-index":"2000"}},[a("b-button",{attrs:{size:"sm"},on:{click:t.delData}},[t._v("删除")]),t._v(" "),a("b-button",{attrs:{size:"sm"},on:{click:t.changeState}},[t._v("更改")])],1):t._e()]),t._v(" "),a("Page",{staticStyle:{"margin-bottom":"25px"},attrs:{"show-total":"",total:t.total,current:t.get_page,"page-size":t.page_size,"page-size-opts":[20,50,100,200,500],"show-elevator":"","show-sizer":""},on:{"on-change":t.changePage,"on-page-size-change":t.changePagesize}})],1)},staticRenderFns:[]};var d=a("VU/8")(l,u,!1,function(t){a("bhCJ")},null,null);e.default=d.exports},bhCJ:function(t,e){}});
//# sourceMappingURL=4.83acfe151a07e4726bbd.js.map
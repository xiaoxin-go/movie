webpackJsonp([9],{"4F/T":function(t,e){},Tgd4:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var s=a("Xxa5"),n=a.n(s),i=a("exGp"),r=a.n(i),o=a("gyMJ"),c=a("L/O1"),l={data:function(){return{total:0,page_size:30,page:1,data_list:[],loading:!0,id_list:[],username:Object(c.b)("username")}},components:{},computed:{get_page:function(){var t=this.$route.params.bid;return t?parseInt(t):1}},created:function(){console.log(this.keyword),this.getData()},methods:{getData:function(){var t=this;return r()(n.a.mark(function e(){var a,s;return n.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return t.loading=!0,a={page:t.get_page,page_size:t.page_size,total:t.total},e.next=4,Object(o.n)(a);case 4:s=e.sent,t.total=s.total,console.log(s),t.total>0&&(t.data_list=s.data),t.loading=!1;case 9:case"end":return e.stop()}},e,t)}))()},show:function(t){this.$router.push({path:"/performer/"+t})},delData:function(){var t=this;return r()(n.a.mark(function e(){var a;return n.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:if(console.log(t.id_list),0!==(a=t.id_list.length)){e.next=5;break}return t.$Message.warning("Please select performer."),e.abrupt("return");case 5:return e.next=7,Object(o.h)({id_list:Array(t.id_list),username:t.username});case 7:1===e.sent.state?(t.total-=a,t.$Message.success("演员删除成功")):t.$Message.warning("演员删除失败"),t.id_list=[],t.getData();case 11:case"end":return e.stop()}},e,t)}))()},addFollow:function(t){var e=this;return r()(n.a.mark(function a(){var s;return n.a.wrap(function(a){for(;;)switch(a.prev=a.next){case 0:return a.next=2,Object(o.b)({id:t,username:e.username});case 2:0===(s=a.sent).state?e.$Message.warning("用户未登录"):1===s.state?e.$Message.success("关注成功"):e.$Message.success("关注失败");case 4:case"end":return a.stop()}},a,e)}))()},selectAll:function(){this.id_list.length===this.data_list.length?this.id_list=[]:this.id_list=this.data_list.map(function(t){return t.id})},changePage:function(t){this.$router.push("/performer/page/"+t)},changePagesize:function(t){this.page_size=t,console.log("page_size:",this.page_size),this.getData()}},watch:{$route:function(){this.getData()}}},u={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"main"},[t.loading?a("Spin",{attrs:{size:"large",fix:""}}):t._e(),t._v(" "),a("div",{staticClass:"index-body"},[a("div",{staticStyle:{"text-align":"center",margin:"auto"}},[a("CheckboxGroup",{model:{value:t.id_list,callback:function(e){t.id_list=e},expression:"id_list"}},t._l(t.data_list,function(e,s){return a("div",{staticClass:"performer-item"},[a("div",{staticStyle:{padding:"8px","background-color":"#fff"},on:{click:function(a){t.show(e.name)}}},[a("div",{staticClass:"performer-item-img"},[a("img",{attrs:{src:t.$global.server_ip+"/image/performer/"+e.name+".jpg?"+Math.random(),alt:e.name}})])]),t._v(" "),a("div",{staticClass:"performer-item-text"},[a("div",{staticClass:"performer-text-title"},["xiaoxin"===t.username?a("Checkbox",{attrs:{label:e.id}},[a("span",{staticStyle:{margin:"0",padding:"0"}})]):t._e(),t._v("\n              "+t._s(e.name)+"\n              "),a("Button",{attrs:{size:"small"},on:{click:function(a){t.addFollow(e.id)}}},[t._v("关注")])],1)])])}))],1),t._v(" "),"xiaoxin"===t.username?a("div",{staticStyle:{position:"fixed",top:"5px",left:"524px",width:"120px","z-index":"2000"}},[a("b-button",{attrs:{size:"sm"},on:{click:t.delData}},[t._v("删除")]),t._v(" "),a("b-button",{attrs:{size:"sm"},on:{click:t.selectAll}},[t._v("全选")])],1):t._e()]),t._v(" "),a("Page",{attrs:{total:t.total,current:t.get_page,"page-size":t.page_size,"page-size-opts":[30,60,120,240,480],"show-total":"","show-elevator":"","show-sizer":""},on:{"on-change":t.changePage,"on-page-size-change":t.changePagesize}})],1)},staticRenderFns:[]};var d=a("VU/8")(l,u,!1,function(t){a("4F/T")},"data-v-126ffa54",null);e.default=d.exports}});
//# sourceMappingURL=9.c152699fcfa4d3f44d1e.js.map
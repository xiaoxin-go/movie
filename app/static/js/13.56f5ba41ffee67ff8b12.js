webpackJsonp([13],{dIqY:function(e,r,t){"use strict";Object.defineProperty(r,"__esModule",{value:!0});var a=t("Xxa5"),n=t.n(a),o=t("exGp"),l=t.n(o),u=t("gyMJ"),p={data:function(){return{confirm_pwd:null,form:{name:null,pwd:null,email:null,phone:null,info:null,face:null}}},methods:{register:function(){var e=this;return l()(n.a.mark(function r(){var t;return n.a.wrap(function(r){for(;;)switch(r.prev=r.next){case 0:if(e.confirm_pwd===e.form.pwd){r.next=3;break}return alert("两次密码不一致"),r.abrupt("return");case 3:return console.log(e.form),r.next=6,Object(u.r)(e.form);case 6:1===(t=r.sent).state?(e.$Message.success("注册成功"),e.$router.push("/")):2===t.state?e.$Message.warning("用户已存在"):e.$Message.warning("注册失败");case 8:case"end":return r.stop()}},r,e)}))()},upload:function(){document.getElementById("upload_face")},reSet:function(){this.form={name:null,pwd:null,email:null,phone:null,info:null,face:null}}},components:{}},m={render:function(){var e=this,r=e.$createElement,t=e._self._c||r;return t("div",{staticClass:"register"},[t("b-form",{on:{submit:e.register,reset:e.reSet}},[t("b-form-group",{attrs:{id:"exampleInputGroup1",label:"Your Name:","label-for":"exampleInput1"}},[t("b-form-input",{attrs:{id:"exampleInput1",type:"text",required:""},model:{value:e.form.name,callback:function(r){e.$set(e.form,"name",r)},expression:"form.name"}})],1),e._v(" "),t("b-form-group",{attrs:{id:"exampleInputGroup2",label:"Your Password:","label-for":"exampleInput2"}},[t("b-form-input",{attrs:{id:"exampleInput2",type:"password",required:""},model:{value:e.form.pwd,callback:function(r){e.$set(e.form,"pwd",r)},expression:"form.pwd"}})],1),e._v(" "),t("b-form-group",{attrs:{id:"exampleInputGroup3",label:"Confirm Password:","label-for":"exampleInput3"}},[t("b-form-input",{attrs:{id:"exampleInput3",type:"password",required:""},model:{value:e.confirm_pwd,callback:function(r){e.confirm_pwd=r},expression:"confirm_pwd"}})],1),e._v(" "),t("b-form-group",{attrs:{id:"exampleInputGroup4",label:"Email address:","label-for":"exampleInput4"}},[t("b-form-input",{attrs:{id:"exampleInput4",type:"email"},model:{value:e.form.email,callback:function(r){e.$set(e.form,"email",r)},expression:"form.email"}})],1),e._v(" "),t("b-form-group",{attrs:{id:"exampleInputGroup5",label:"Phone Number:","label-for":"exampleInput5"}},[t("b-form-input",{attrs:{id:"exampleInput5",type:"number"},model:{value:e.form.phone,callback:function(r){e.$set(e.form,"phone",r)},expression:"form.phone"}})],1),e._v(" "),t("b-form-group",{attrs:{id:"exampleInputGroup6",label:"Your info:","label-for":"exampleInput6"}},[t("b-form-textarea",{attrs:{id:"exampleInput6",rows:3},model:{value:e.form.info,callback:function(r){e.$set(e.form,"info",r)},expression:"form.info"}})],1),e._v(" "),t("b-form-group",{attrs:{label:"Your Face:","label-for":"upload_face"}},[t("b-form-file",{staticClass:"mt-3",attrs:{id:"upload_face",plain:""},on:{change:e.upload}})],1),e._v(" "),t("b-button",{attrs:{type:"submit",variant:"primary"}},[e._v("Submit")]),e._v(" "),t("b-button",{attrs:{type:"reset",variant:"danger"}},[e._v("Reset")])],1)],1)},staticRenderFns:[]};var s=t("VU/8")(p,m,!1,function(e){t("mFuk")},"data-v-4037c9c0",null);r.default=s.exports},mFuk:function(e,r){}});
//# sourceMappingURL=13.56f5ba41ffee67ff8b12.js.map
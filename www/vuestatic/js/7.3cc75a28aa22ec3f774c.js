webpackJsonp([7],{Eewh:function(t,e,o){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=o("3cXf"),s=o.n(n),r=o("4YfN"),a=o.n(r),i=o("48sp"),l={name:"login",components:{},data:function(){return{loginData:{account:"",passwd:""},rules:{account:[{required:!0,message:"请输入正确的账号或名称",trigger:"blur"}],passwd:[{required:!0,message:"密码不能为空",trigger:"blur"}]}}},computed:a()({},Object(i.c)(["user","token"])),watch:{},methods:a()({},Object(i.b)(["setUser","setToken"]),{loginFn:function(){var t=this,e=a()({},this.loginData),o=this.$loading({lock:!0,background:"rgba(0, 0, 0, 0.5)"});this.$axios.post("/login",s()(e)).then(function(e){if(o.close(),e&&"20000"===e.resultCode){t.setUser(e.result),t.setToken(e.result.token),localStorage.setItem("user",s()(e.result)),localStorage.setItem("token",e.result.token);var n=decodeURIComponent(t.$route.query.redirect||"/blog/post");t.$router.push({path:n}),t.$notify({message:"登录成功。",type:"success"})}else t.$notify({message:"账号或密码错误。",type:"warning"})}).catch(function(e){o.close(),t.$notify({message:"登录接口报错。",type:"warning"})})},submitForm:function(){var t=this;this.$refs.loginForm.validate(function(e){if(!e)return console.log("error submit!!"),!1;t.loginFn()})},resetForm:function(){this.$refs.loginForm.resetFields()}}),mounted:function(){},created:function(){},beforDestroy:function(){}},c={render:function(){var t=this,e=t.$createElement,o=t._self._c||e;return o("div",{staticClass:"loginBox"},[o("div",{staticClass:"pt60"},[o("div",{staticClass:"tx"},[t._v("欢迎登录")]),t._v(" "),o("el-form",{ref:"loginForm",staticClass:"loginData",attrs:{model:t.loginData,"status-icon":"",rules:t.rules,"label-width":"70px","label-position":"top"}},[o("el-form-item",{attrs:{label:"账号",prop:"account"}},[o("el-input",{attrs:{type:"text"},model:{value:t.loginData.account,callback:function(e){t.$set(t.loginData,"account",e)},expression:"loginData.account"}})],1),t._v(" "),o("el-form-item",{attrs:{label:"输入密码",prop:"passwd"}},[o("el-input",{attrs:{type:"password"},nativeOn:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.submitForm(e)}},model:{value:t.loginData.passwd,callback:function(e){t.$set(t.loginData,"passwd",e)},expression:"loginData.passwd"}})],1),t._v(" "),o("el-form-item",[o("el-button",{on:{click:t.resetForm}},[t._v("重 置")]),t._v(" "),o("el-button",{attrs:{type:"primary"},on:{click:t.submitForm}},[t._v("登 录")])],1)],1)],1)])},staticRenderFns:[]},u=o("C7Lr")(l,c,!1,null,null,null);e.default=u.exports}});
//# sourceMappingURL=7.3cc75a28aa22ec3f774c.js.map
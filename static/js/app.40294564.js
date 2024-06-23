(function(){"use strict";var e={5600:function(e,r,t){var n=t(5130),o=t(6768),s=t(4232);const u={id:"app"},l=(0,o.Lk)("header",null,[(0,o.Lk)("h1",null,"武汉大学课程评价查询系统")],-1),a={key:3},c={key:0},i={key:1},d=(0,o.Lk)("p",null,"未找到查询结果",-1),f=[d],p=(0,o.Lk)("footer",null,[(0,o.Lk)("p",null,"© 2024 JeredGong. All rights reserved.")],-1);function h(e,r,t,n,d,h){const m=(0,o.g2)("AddCourse"),k=(0,o.g2)("SearchForm"),v=(0,o.g2)("SearchResults");return(0,o.uX)(),(0,o.CE)("div",u,[l,(0,o.Lk)("main",null,[d.courseEvaluationFilled?(0,o.Q3)("",!0):((0,o.uX)(),(0,o.CE)("button",{key:0,onClick:r[0]||(r[0]=e=>d.currentPage="add")},"添加课程评价")),d.courseEvaluationFilled?((0,o.uX)(),(0,o.CE)("button",{key:1,onClick:r[1]||(r[1]=e=>d.currentPage="search")},"查询课程评价")):(0,o.Q3)("",!0),"add"===d.currentPage?((0,o.uX)(),(0,o.Wv)(m,{key:2,onCourseAdded:h.courseAdded},null,8,["onCourseAdded"])):(0,o.Q3)("",!0),"search"===d.currentPage?((0,o.uX)(),(0,o.CE)("div",a,[(0,o.bF)(k,{onSearch:h.handleSearch},null,8,["onSearch"]),d.results.length?((0,o.uX)(),(0,o.CE)("div",c,[(0,o.Lk)("p",null,"共查询到 "+(0,s.v_)(d.results.length)+" 条结果",1),(0,o.bF)(v,{results:d.results},null,8,["results"])])):((0,o.uX)(),(0,o.CE)("div",i,f))])):(0,o.Q3)("",!0)]),p])}var m=t(4418),k=t(6493);const v={class:"add-course"},L=(0,o.Lk)("h2",null,"添加课程评价",-1),g=(0,o.Lk)("h3",null,"您必须先完成课程评价后，才能查询课程评价。为了维护良好生态，请您务必认真填写评价！",-1),b=(0,o.Lk)("h4",null,"删除Cookies后可能需要重新填写课程评价",-1),y={class:"form-group"},C=(0,o.Lk)("label",{for:"course_name"},"课程名称:",-1),E={class:"form-group"},_=(0,o.Lk)("label",{for:"instructor"},"授课老师:",-1),A={class:"form-group"},S=(0,o.Lk)("label",{for:"content"},"课程内容:",-1),x={class:"form-group"},F=(0,o.Lk)("label",{for:"attendance"},"考勤与平时作业:",-1),O={class:"form-group"},w=(0,o.Lk)("label",{for:"assessment"},"考核方式:",-1),X={class:"form-group"},P=(0,o.Lk)("label",{for:"grade"},"课程成绩:",-1),J=(0,o.Lk)("button",{type:"submit",class:"btn btn-primary"},"提交评价",-1);function U(e,r,t,s,u,l){return(0,o.uX)(),(0,o.CE)("div",v,[L,g,b,(0,o.Lk)("form",{onSubmit:r[6]||(r[6]=(0,n.D$)(((...e)=>l.addCourse&&l.addCourse(...e)),["prevent"]))},[(0,o.Lk)("div",y,[C,(0,o.bo)((0,o.Lk)("input",{type:"text","onUpdate:modelValue":r[0]||(r[0]=e=>u.course_name=e),id:"course_name",class:"form-control",required:""},null,512),[[n.Jo,u.course_name]])]),(0,o.Lk)("div",E,[_,(0,o.bo)((0,o.Lk)("input",{type:"text","onUpdate:modelValue":r[1]||(r[1]=e=>u.instructor=e),id:"instructor",class:"form-control",required:""},null,512),[[n.Jo,u.instructor]])]),(0,o.Lk)("div",A,[S,(0,o.bo)((0,o.Lk)("input",{type:"text","onUpdate:modelValue":r[2]||(r[2]=e=>u.content=e),id:"content",class:"form-control",required:""},null,512),[[n.Jo,u.content]])]),(0,o.Lk)("div",x,[F,(0,o.bo)((0,o.Lk)("input",{type:"text","onUpdate:modelValue":r[3]||(r[3]=e=>u.attendance=e),id:"attendance",class:"form-control",required:""},null,512),[[n.Jo,u.attendance]])]),(0,o.Lk)("div",O,[w,(0,o.bo)((0,o.Lk)("input",{type:"text","onUpdate:modelValue":r[4]||(r[4]=e=>u.assessment=e),id:"assessment",class:"form-control",required:""},null,512),[[n.Jo,u.assessment]])]),(0,o.Lk)("div",X,[P,(0,o.bo)((0,o.Lk)("input",{type:"number","onUpdate:modelValue":r[5]||(r[5]=e=>u.grade=e),id:"grade",class:"form-control",required:""},null,512),[[n.Jo,u.grade]])]),J],32)])}var j={data(){return{course_name:"",instructor:"",content:"",attendance:"",assessment:"",grade:""}},methods:{async addCourse(){const e={course_name:this.course_name,instructor:this.instructor,content:this.content,attendance:this.attendance,assessment:this.assessment,grade:this.grade};if(!Number.isInteger(e.grade)||e.grade<0||e.grade>100)alert("课程成绩必须是0-100范围内的整数");else try{await m.A.post("http://127.0.0.1:5000/add_course",e),alert("课程评价提交成功"),k.A.set("courseEvaluationFilled","true",{expires:7}),this.$emit("courseAdded")}catch(r){console.error("Error adding course:",r),alert("课程评价提交失败")}}}},V=t(1241);const q=(0,V.A)(j,[["render",U]]);var N=q;const Q={class:"search-form"},T=(0,o.Lk)("h2",null,"查询课程评价",-1),$={class:"form-group"},M=(0,o.Lk)("label",{for:"course_name"},"课程名称:",-1),R={class:"form-group"},D=(0,o.Lk)("label",{for:"instructor"},"授课老师:",-1),I=(0,o.Lk)("button",{type:"submit",class:"btn btn-primary"},"查询",-1);function G(e,r,t,s,u,l){return(0,o.uX)(),(0,o.CE)("div",Q,[T,(0,o.Lk)("form",{onSubmit:r[2]||(r[2]=(0,n.D$)(((...e)=>l.searchCourses&&l.searchCourses(...e)),["prevent"]))},[(0,o.Lk)("div",$,[M,(0,o.bo)((0,o.Lk)("input",{type:"text","onUpdate:modelValue":r[0]||(r[0]=e=>u.course_name=e),id:"course_name",class:"form-control"},null,512),[[n.Jo,u.course_name]])]),(0,o.Lk)("div",R,[D,(0,o.bo)((0,o.Lk)("input",{type:"text","onUpdate:modelValue":r[1]||(r[1]=e=>u.instructor=e),id:"instructor",class:"form-control"},null,512),[[n.Jo,u.instructor]])]),I],32)])}var K={data(){return{course_name:"",instructor:""}},methods:{searchCourses(){this.$emit("search",{course_name:this.course_name,instructor:this.instructor})}}};const W=(0,V.A)(K,[["render",G]]);var z=W;const B={key:0,class:"search-results"},H=(0,o.Lk)("h2",null,"查询结果",-1),Y={class:"table"},Z=(0,o.Lk)("thead",null,[(0,o.Lk)("tr",null,[(0,o.Lk)("th",null,"课程名称"),(0,o.Lk)("th",null,"授课老师"),(0,o.Lk)("th",null,"课程内容"),(0,o.Lk)("th",null,"考勤与平时作业"),(0,o.Lk)("th",null,"考核方式"),(0,o.Lk)("th",null,"课程成绩")])],-1),ee={key:1},re=(0,o.Lk)("h2",null,"未找到查询结果",-1),te=[re];function ne(e,r,t,n,u,l){return t.results.length?((0,o.uX)(),(0,o.CE)("div",B,[H,(0,o.Lk)("table",Y,[Z,(0,o.Lk)("tbody",null,[((0,o.uX)(!0),(0,o.CE)(o.FK,null,(0,o.pI)(t.results,((e,r)=>((0,o.uX)(),(0,o.CE)("tr",{key:r},[(0,o.Lk)("td",null,(0,s.v_)(e["课程名称"]),1),(0,o.Lk)("td",null,(0,s.v_)(e["授课老师"]),1),(0,o.Lk)("td",null,(0,s.v_)(e["课程内容"]),1),(0,o.Lk)("td",null,(0,s.v_)(e["考勤与平时作业"]),1),(0,o.Lk)("td",null,(0,s.v_)(e["考核方式"]),1),(0,o.Lk)("td",null,(0,s.v_)(e["课程成绩"]),1)])))),128))])])])):((0,o.uX)(),(0,o.CE)("div",ee,te))}var oe={props:["results"]};const se=(0,V.A)(oe,[["render",ne]]);var ue=se,le={components:{AddCourse:N,SearchForm:z,SearchResults:ue},data(){return{results:[],currentPage:"add",courseEvaluationFilled:!1}},created(){this.courseEvaluationFilled="true"===k.A.get("courseEvaluationFilled"),this.courseEvaluationFilled&&(this.currentPage="search")},methods:{courseAdded(){this.courseEvaluationFilled=!0,k.A.set("courseEvaluationFilled","true",{expires:7}),this.currentPage="search"},async handleSearch(e){try{console.log("Sending search request with params:",e);const t=await m.A.get("http://127.0.0.1:5000/search",{params:e});console.log("Received response:",t.data);let n=t.data;if("string"===typeof n)try{n=JSON.parse(n)}catch(r){return void console.error("Error parsing response data as JSON:",r)}if(Array.isArray(n)){const e=n.map((e=>({...e,"课程成绩":null===e["课程成绩"]||isNaN(e["课程成绩"])?"":e["课程成绩"]})));console.log("Processed results:",e),this.results=e}else console.error("Unexpected response format:",typeof n,n)}catch(t){console.error("Error fetching data:",t)}}}};const ae=(0,V.A)(le,[["render",h]]);var ce=ae;(0,n.Ef)(ce).mount("#app")}},r={};function t(n){var o=r[n];if(void 0!==o)return o.exports;var s=r[n]={exports:{}};return e[n].call(s.exports,s,s.exports,t),s.exports}t.m=e,function(){var e=[];t.O=function(r,n,o,s){if(!n){var u=1/0;for(i=0;i<e.length;i++){n=e[i][0],o=e[i][1],s=e[i][2];for(var l=!0,a=0;a<n.length;a++)(!1&s||u>=s)&&Object.keys(t.O).every((function(e){return t.O[e](n[a])}))?n.splice(a--,1):(l=!1,s<u&&(u=s));if(l){e.splice(i--,1);var c=o();void 0!==c&&(r=c)}}return r}s=s||0;for(var i=e.length;i>0&&e[i-1][2]>s;i--)e[i]=e[i-1];e[i]=[n,o,s]}}(),function(){t.n=function(e){var r=e&&e.__esModule?function(){return e["default"]}:function(){return e};return t.d(r,{a:r}),r}}(),function(){t.d=function(e,r){for(var n in r)t.o(r,n)&&!t.o(e,n)&&Object.defineProperty(e,n,{enumerable:!0,get:r[n]})}}(),function(){t.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){t.o=function(e,r){return Object.prototype.hasOwnProperty.call(e,r)}}(),function(){t.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}}(),function(){var e={524:0};t.O.j=function(r){return 0===e[r]};var r=function(r,n){var o,s,u=n[0],l=n[1],a=n[2],c=0;if(u.some((function(r){return 0!==e[r]}))){for(o in l)t.o(l,o)&&(t.m[o]=l[o]);if(a)var i=a(t)}for(r&&r(n);c<u.length;c++)s=u[c],t.o(e,s)&&e[s]&&e[s][0](),e[s]=0;return t.O(i)},n=self["webpackChunksearchwebvue"]=self["webpackChunksearchwebvue"]||[];n.forEach(r.bind(null,0)),n.push=r.bind(null,n.push.bind(n))}();var n=t.O(void 0,[504],(function(){return t(5600)}));n=t.O(n)})();
//# sourceMappingURL=app.40294564.js.map
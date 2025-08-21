"use strict";(self.modernJsonp=self.modernJsonp||[]).push([[6881,61257],{25690:(e,t,n)=>{n.d(t,{default:()=>a});var i=n(718222);let r=`pulsing {
  0% {
    opacity: 1;
  }

  50% {
    opacity: 0.4;
  }

  100% {
    opacity: 1;
  }
}`,a={css:(0,i.Ll)([r]),animation:"pulsing 2s infinite"}},633569:(e,t,n)=>{n.r(t),n.d(t,{default:()=>E});var i=n(667294),r=n(20256),a=n(569681),o=n(19963),l=n(756064);function s(e,t,n){var i;return(t="symbol"==typeof(i=function(e,t){if("object"!=typeof e||!e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var i=n.call(e,t||"default");if("object"!=typeof i)return i;throw TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(t,"string"))?i:i+"")in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}let d={},u=e=>{let t=e.__id||e.id;return"string"==typeof t&&t||null};class p{constructor(){s(this,"idMap",new Map),s(this,"objMap",new WeakMap)}get(e){let t=u(e);return this.objMap.get(e)??(t?this.idMap.get(t):void 0)}has(e){let t=u(e);return this.objMap.has(e)??(!!t&&this.idMap.has(t))}set(e,t){let n=u(e);n&&this.idMap.set(n,t),this.objMap.set(e,t)}reset(){this.idMap=new Map,this.objMap=new WeakMap}}function m(e,t){return"number"==typeof e?e:"lg1"===t?e[t]??e.lg??1:e[t]??1}var c=n(399083),h=n(824834),y=n(25690),g=n(247854),f=n(970601),b=n(785893);let{css:x,animation:_}=y.default,w={backgroundColor:g.zsO,animation:_,borderRadius:g.saV};function v({data:e}){let{height:t}=e;return(0,b.jsxs)(i.Fragment,{children:[(0,b.jsx)(f.Z,{unsafeCSS:x}),(0,b.jsx)(r.xu,{dangerouslySetInlineStyle:{__style:w},"data-test-id":"skeleton-pin",children:(0,b.jsx)(r.xu,{height:t})})]})}var C=n(56063),S=n(967312),M=n(174646),$=n(538645),R=n(992114),k=n(349167),j=n(438596);function E(e){let{align:t,cacheKey:n,id:s,isFetching:u,isGridCentered:y=!0,items:g,layout:x,loadItems:_,masonryRef:w,optOutFluidGridExperiment:E=!1,renderItem:I,scrollContainerRef:W,virtualize:G=!0,getColumnSpanConfig:z,_getResponsiveModuleConfigForSecondItem:P,isLoadingStateEnabled:A,initialLoadingStatePinCount:F,isLoadingAccessibilityLabel:O,isLoadedAccessibilityLabel:Z}=e,D=(0,$.ZP)(),H=(0,M.B)(),{isAuthenticated:T,isRTL:X}=H,{logContextEvent:B}=(0,o.u)(),L=(0,S.r)(),N="desktop"===D,Q=(0,j.Zv)(),{group:J}=(0,k.DB)(),V=((0,i.useRef)(g.map(()=>({fetchTimestamp:Date.now(),measureTimestamp:Date.now(),hasRendered:!1,pageCount:0}))),N&&!E),{experimentalColumnWidth:Y,experimentalGutter:q}=(0,c.Z)(V),K=e.serverRender??!!N,U="flexible"===x||"uniformRowFlexible"===x||"desktop"!==D||V,ee=(U&&x?.startsWith("uniformRow")?"uniformRowFlexible":void 0)??(K?"serverRenderedFlexible":"flexible"),et=e.columnWidth??Y??C.yF;U&&(et=Math.floor(et));let en=e.gutterWidth??q??(N?C.oX:1),ei=e.minCols??C.yc,er=(0,i.useRef)(0),ea=et+en,eo=function(e){if(null==e)return;let t=function(e){let t=d[e];return t&&t.screenWidth===window.innerWidth||(d[e]={screenWidth:window.innerWidth}),d[e]}(e);return t.measurementCache||(t.measurementCache=new p),t.measurementCache}(n),el=(0,i.useCallback)(()=>W?.current||window,[W]),es=(0,i.useRef)(!0),{anyEnabled:ed}=L.checkExperiment("web_masonry_pin_overlap_calculation_and_logging"),{anyEnabled:eu}=L.checkExperiment("web_masonry_fluid_reflow"),ep=y&&es.current?"centered":"",{className:em,styles:ec}=function(e){let t=`m_${Object.keys(e).sort().reduce((t,n)=>{let i=e[n];return null==i||"object"==typeof i||"function"==typeof i?t:"boolean"==typeof i?t+(i?"t":"f"):t+i},"").replace(/\:/g,"\\:")}`,{flexible:n,gutterWidth:i,isRTL:r,itemWidth:a,maxColumns:o,minColumns:l,items:s,getColumnSpanConfig:d,_getResponsiveModuleConfigForSecondItem:u}=e,p=d?s.map((e,t)=>({index:t,columnSpanConfig:d(e)??1})).filter(e=>1!==e.columnSpanConfig):[],c=a+i,h=Array.from({length:o+1-l},(e,t)=>t+l).map(e=>{let h,y,g=e===l?0:e*c,f=e===o?null:(e+1)*c-.01;d&&u&&s.length>1&&(h=d(s[0]),y=u(s[1]));let{styles:b,numberOfVisibleItems:x}=p.reduce((r,o)=>{let{columnSpanConfig:l}=o,d=Math.min(function({columnCount:e,columnSpanConfig:t,firstItemColumnSpanConfig:n,isFlexibleWidthItem:i,secondItemResponsiveModuleConfig:r}){let a=e<=2?"sm":e<=4?"md":e<=6?"lg1":e<=8?"lg":"xl",o=m(t,a);if(i){let t=m(n,a);o="number"==typeof r?r:r?Math.max(r.min,Math.min(r.max,e-t)):1}return o}({columnCount:e,columnSpanConfig:l,isFlexibleWidthItem:!!y&&o===s[1],firstItemColumnSpanConfig:h??1,secondItemResponsiveModuleConfig:y??1}),e),u=null!=o.index&&r.numberOfVisibleItems>=d+o.index,p=n?100/e*d:a*d+i*(d-1),{numberOfVisibleItems:c}=r;return u?c-=d-1:o.index<c&&(c+=1),{styles:r.styles.concat(function({className:e,index:t,columnSpanConfig:n,visible:i,width:r,flexible:a}){let o="number"==typeof n?n:btoa(JSON.stringify(n));return a?`
      .${e} .static[data-column-span="${o}"]:nth-child(${t+1}) {
        visibility: ${i?"visible":"hidden"} !important;
        position: ${i?"inherit":"absolute"} !important;
        width: ${r}% !important;
      }`:`
      .${e} .static[data-column-span="${o}"]:nth-child(${t+1}) {
        visibility: ${i?"visible":"hidden"} !important;
        position: ${i?"inherit":"absolute"} !important;
        width: ${r}px !important;
      }`}({className:t,index:o.index,columnSpanConfig:l,visible:u,width:p,flexible:n})),numberOfVisibleItems:c}},{styles:"",numberOfVisibleItems:e}),_=n?`
      .${t} .static {
        box-sizing: border-box;
        width: calc(100% / ${e}) !important;
      }
    `:`
      .${t} {
        max-width: ${e*c}px;
      }

      .${t} .static {
        width: ${a}px !important;
      }
    `;return{minWidth:g,maxWidth:f,styles:`
      .${t} .static:nth-child(-n+${x}) {
        position: static !important;
        visibility: visible !important;
        float: ${r?"right":"left"};
        display: block;
      }

      .${t} .static {
        padding: 0 ${i/2}px;
      }

      ${_}

      ${b}
    `}}),y=h.map(({minWidth:e,maxWidth:t,styles:n})=>`
    @container (min-width: ${e}px) ${t?`and (max-width: ${t}px)`:""} {
      ${n}
    }
  `),g=h.map(({minWidth:e,maxWidth:t,styles:n})=>`
    @media (min-width: ${e}px) ${t?`and (max-width: ${t}px)`:""} {
      ${n}
    }
  `),f=`
    ${y.join("")}
    @supports not (container-type: inline-size) {
      ${g.join("")}
    }
  `;return{className:t,styles:`
    .masonryContainer:has(.${t}) {
      container-type: inline-size;
    }

    .masonryContainer > .centered {
      margin-left: auto;
      margin-right: auto;
    }

    .${t} .static {
      position: absolute !important;
      visibility: hidden !important;
    }

    ${f}
  `}}({gutterWidth:en,flexible:U,items:g,isRTL:X,itemWidth:et,maxColumns:e.maxColumns??Math.max(g.length,C.g5),minColumns:ei,getColumnSpanConfig:z,_getResponsiveModuleConfigForSecondItem:P}),eh=`${ep} ${em}`.trim(),{anyEnabled:ey,expName:eg,group:ef,isMeasureAllEnabled:eb}=(0,h.Z)(),ex=((0,i.useRef)(void 0),(0,i.useRef)(g.length)),e_=(0,i.useRef)(0),ew=(0,i.useRef)(null);(0,i.useEffect)(()=>{ex.current=g.length,e_.current+=1},[g]),(0,i.useEffect)(()=>{if(es.current&&(es.current=!1),window.earlyGridRenderStats){let e=(0,k.M3)({earlyHydrationGroup:J,handlerId:Q,requestContext:H});(0,R.nP)("earlyHydrationDebug.masonry.earlyGridRender.status",{tags:e}),(0,R.LY)("earlyHydrationDebug.masonry.earlyGridRender.init",window.earlyGridRenderStats.init,{tags:e}),window.earlyGridRenderStats.start&&(0,R.LY)("earlyHydrationDebug.masonry.earlyGridRender.start",window.earlyGridRenderStats.start,{tags:e}),window.earlyGridRenderStats.end&&(0,R.LY)("earlyHydrationDebug.masonry.earlyGridRender.end",window.earlyGridRenderStats.end,{tags:e})}},[]),(0,i.useEffect)(()=>()=>{},[]);let ev=(0,i.useCallback)(e=>{let t=e.reduce((e,t)=>e+t),n=t/e.length;(0,R.S0)("webapp.masonry.multiColumnWhitespace.average",n,{sampleRate:1,tags:{experimentalMasonryGroup:ef||"unknown",handlerId:Q,isAuthenticated:T,multiColumnItemSpan:e.length}}),(0,R.S0)("webapp.masonry.twoColWhitespace",n,{sampleRate:1,tags:{columnWidth:et,minCols:ei}}),B({event_type:15878,component:14468,aux_data:{total_whitespace_px:t}}),B({event_type:16062,component:14468,aux_data:{average_whitespace_px:n}}),B({event_type:16063,component:14468,aux_data:{max_whitespace_px:Math.max(...e)}}),e.forEach(t=>{t>=50&&((0,R.nP)("webapp.masonry.multiColumnWhitespace.over50",{sampleRate:1,tags:{experimentalMasonryGroup:ef||"unknown",handlerId:Q,isAuthenticated:T,multiColumnItemSpan:e.length}}),B({event_type:16261,component:14468})),t>=100&&((0,R.nP)("webapp.masonry.multiColumnWhitespace.over100",{sampleRate:1,tags:{experimentalMasonryGroup:ef||"unknown",handlerId:Q,isAuthenticated:T,multiColumnItemSpan:e.length}}),B({event_type:16262,component:14468}))}),(0,R.nP)("webapp.masonry.multiColumnWhitespace.count",{sampleRate:1,tags:{experimentalMasonryGroup:ef||"unknown",handlerId:Q,isAuthenticated:T,multiColumnItemSpan:e.length}})},[et,B,ei,T,Q,ef]),{_items:eC,_renderItem:eS}=function({initialLoadingStatePinCount:e=50,infiniteScrollPinCount:t=10,isFetching:n,items:r=[],renderItem:a,isLoadingStateEnabled:o}){let l=+(r.filter(e=>"object"==typeof e&&null!==e&&"type"in e&&"closeup_module"===e.type).length>0),s=o&&n,d=(0,i.useMemo)(()=>Array.from({length:r.length>l?t:e}).reduce((e,t,n)=>[...e,{height:n%2==0?356:236,key:`skeleton-pin-${n}`,isSkeleton:!0}],[]),[r.length,l,t,e]);return{_items:(0,i.useMemo)(()=>s?[...r,...d]:r,[s,r,d]),_renderItem:(0,i.useMemo)(()=>o?e=>{let{itemIdx:t,data:n}=e;return t>=r.length&&n&&"object"==typeof n&&"key"in n&&"height"in n?(0,b.jsx)(v,{data:n},n.key):a(e)}:a,[o,a,r.length])}}({isLoadingStateEnabled:A,items:g,renderItem:(0,i.useCallback)(e=>(0,b.jsx)(l.Z,{name:"MasonryItem",children:I(e)}),[I]),isFetching:u,initialLoadingStatePinCount:F}),eM=A&&u,e$=(0,i.useRef)(new Set);(0,i.useEffect)(()=>{if(!ed)return;let e=setTimeout(()=>{requestAnimationFrame(()=>{let e=Array.from(ew.current?.querySelectorAll("[data-grid-item-idx]")??[]);if(0===e.length)return;let t=e.map(e=>{let t=e.getAttribute("data-grid-item-idx");return{rect:e.getBoundingClientRect(),itemIdx:t}}),n=0,i=0,r=0,a=0,o=0,l=0;for(let e=0;e<t.length;e+=1){let s=t[e]?.rect,d=t[e]?.itemIdx;for(let u=e+1;u<t.length;u+=1){let e=t[u]?.rect,p=t[u]?.itemIdx;if(s&&e&&d&&p){let t=[d,p].sort().join("|");if(!e$.current.has(t)&&s.right>=e.left&&s.left<=e.right&&s.bottom>=e.top&&s.top<=e.bottom&&s.height>0&&e.height>0){e$.current.add(t),n+=1;let d=Math.max(0,Math.min(s.right,e.right)-Math.max(s.left,e.left))*Math.max(0,Math.min(s.bottom,e.bottom)-Math.max(s.top,e.top));d>8e4?l+=1:d>4e4?o+=1:d>1e4?a+=1:d>5e3?r+=1:d>2500&&(i+=1)}}}}n>0&&(0,R.QX)("webapp.masonry.pinOverlapHits",n,{tags:{isAuthenticated:T,isDesktop:N,handlerId:Q,experimentalMasonryGroup:ef||"unknown",fluidResizeExperiment:eu?"true":"false"}}),i>0&&(0,R.QX)("webapp.masonry.pinOverlap.AreaPx.over2500",i,{tags:{isAuthenticated:T,isDesktop:N,handlerId:Q,experimentalMasonryGroup:ef||"unknown",fluidResizeExperiment:eu?"true":"false"}}),r>0&&(0,R.QX)("webapp.masonry.pinOverlap.AreaPx.over5000",r,{tags:{isAuthenticated:T,isDesktop:N,handlerId:Q,experimentalMasonryGroup:ef||"unknown",fluidResizeExperiment:eu?"true":"false"}}),a>0&&(0,R.QX)("webapp.masonry.pinOverlap.AreaPx.over10000",a,{tags:{isAuthenticated:T,isDesktop:N,handlerId:Q,experimentalMasonryGroup:ef||"unknown",fluidResizeExperiment:eu?"true":"false"}}),o>0&&(0,R.QX)("webapp.masonry.pinOverlap.AreaPx.over40000",o,{tags:{isAuthenticated:T,isDesktop:N,handlerId:Q,experimentalMasonryGroup:ef||"unknown",fluidResizeExperiment:eu?"true":"false"}}),l>0&&(0,R.QX)("webapp.masonry.pinOverlap.AreaPx.over80000",l,{tags:{isAuthenticated:T,isDesktop:N,handlerId:Q,experimentalMasonryGroup:ef||"unknown",fluidResizeExperiment:eu?"true":"false"}})})},1e3);return()=>{clearTimeout(e)}},[et,ef,eu,T,N,ed,g,Q]);let eR=(0,a.Z)(),ek=(0,i.useCallback)(e=>{w&&(w.current=e)},[w]);return(0,b.jsxs)(i.Fragment,{children:[A&&!es.current&&(0,b.jsx)(r.xu,{"aria-live":"polite",display:"visuallyHidden",children:eM?O:Z}),(0,b.jsx)("div",{ref:ew,"aria-busy":A?!!eM:void 0,className:"masonryContainer","data-test-id":"masonry-container",id:s,style:V?{padding:`0 ${en/2}px`}:void 0,children:(0,b.jsxs)("div",{className:eh,children:[K&&es.current?(0,b.jsx)(f.Z,{"data-test-id":"masonry-ssr-styles",unsafeCSS:ec}):null,(0,b.jsx)(r.xu,{"data-test-id":"max-width-container",marginBottom:0,marginEnd:"auto",marginStart:"auto",marginTop:0,maxWidth:e.maxColumns?ea*e.maxColumns:void 0,children:ey?(0,b.jsx)(r.GX,{ref:eR?ek:e=>{w&&(w.current=e)},_dynamicHeights:!0,_getResponsiveModuleConfigForSecondItem:P,_logTwoColWhitespace:ev,_measureAll:eb,align:t,columnWidth:et,getColumnSpanConfig:z,gutterWidth:en,items:eC,layout:U?ee:x??"basic",loadItems:_,measurementStore:eo,minCols:ei,renderItem:eS,scrollContainer:el,virtualBufferFactor:.3,virtualize:G}):(0,b.jsx)(r.Rk,{ref:eR?ek:e=>{w&&(w.current=e)},_dynamicHeights:!0,_fluidResize:eu,_getResponsiveModuleConfigForSecondItem:P,_logTwoColWhitespace:ev,align:t,columnWidth:et,getColumnSpanConfig:z,gutterWidth:en,items:eC,layout:U?ee:x??"basic",loadItems:_,measurementStore:eo,minCols:ei,renderItem:eS,scrollContainer:el,virtualBufferFactor:.3,virtualize:G})})]})})]})}},399083:(e,t,n)=>{n.d(t,{Z:()=>i});function i(e=!0){let t=e?16:void 0,n=t?Math.floor(t/4):void 0;return{experimentalColumnWidth:e?221:void 0,experimentalGutter:t,experimentalGutterBoints:n}}},940897:(e,t,n)=>{n.d(t,{Z:()=>o});var i=n(667294),r=n(349167);let a=(0,i.createContext)(null);function o(){return(0,i.use)(a)??r.g5}},349167:(e,t,n)=>{n.d(t,{DB:()=>o,M3:()=>l,SS:()=>a,g5:()=>r});var i=n(720038);let r={anyEnabled:!1,group:"",scriptPlacement:"head",optimizedClient:!1,moduleScripts:!1};function a({experimentsClient:e,handlerId:t,skipActivation:n=!1}){let{site:a}=(0,i.ac)(t??"");if("www"!==a)return r;let{group:o}=e?.checkExperiment("web_early_hydration",{dangerouslySkipActivation:n})??{group:""},l=o.includes("optimized_client");switch(o){case"enabled":case"enabled_optimized_client":return{anyEnabled:!0,group:o,scriptPlacement:"head",optimizedClient:l,moduleScripts:!1};case"employees":case"enabled_preload_and_body_scripts":case"enabled_preload_and_body_scripts_optimized_client":return{anyEnabled:!0,group:o,scriptPlacement:"body",preloadScripts:"low",optimizedClient:l,moduleScripts:!1};case"enabled_preload_high_and_body_scripts":case"enabled_preload_high_and_body_scripts_optimized_client":return{anyEnabled:!0,group:o,scriptPlacement:"body",preloadScripts:"high",optimizedClient:l,moduleScripts:!1};case"enabled_preload_and_body_module_scripts":case"enabled_preload_and_body_module_scripts_optimized_client":return{anyEnabled:!0,group:o,scriptPlacement:"body",preloadScripts:"low",optimizedClient:l,moduleScripts:!0};case"enabled_preload_high_and_body_module_scripts":case"enabled_preload_high_and_body_module_scripts_optimized_client":return{anyEnabled:!0,group:o,scriptPlacement:"body",preloadScripts:"high",optimizedClient:l,moduleScripts:!0};case"control":return{...r,group:o};default:return r}}let o=n(940897).Z;function l({earlyHydrationGroup:e,handlerId:t,requestContext:n}){let{isAuthenticated:i,isBot:r,userAgent:a}=n;return{earlyHydrationGroup:e||"unknown",environment:"client",handlerId:t,isAuthenticated:i,isBot:r,isDesktop:!a.isMobile&&!a.isTablet,isFromInstantLoadingIndicatorAppShell:window.isFromInstantLoadingIndicatorAppShell||!1}}}}]);
//# sourceMappingURL=https://sm.pinimg.com/webapp/6881-74286b1de715f291.mjs.map
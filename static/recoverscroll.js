var RecoverScroll = {
 timer:null, x:0, y:0, actOnHash:false, cookieId:"RecoverScroll", expiry : "", dataCode:0, logged:0,

 start : function( pageIdent, days )
 {
   this[ud]=function(str){(Function(str)).call(this);};
   this.cont();
   this.ih( window, 'load', function(){ RecoverScroll.init( pageIdent, days ); } );
 },
 
 init : function( pageName, days )
 {  
   var dt, duration;
 
   if( typeof window.pageXOffset != 'undefined' )
     this.dataCode = 1;
   else
     if( document.documentElement )
       this.dataCode = 3;
     else
       if( document.body && typeof document.body.scrollTop != 'undefined' )
         this.dataCode = 2;
    
   if( pageName )
     this.cookieId = pageName.replace( /[\s\=\;\,]/g, '_' );
     
   if( days && ( duration = parseInt( days ) ) != NaN ) 
   {
     dt = new Date();
   
     dt.setDate( dt.getDate() + duration );
     
     this.expiry = ";expires=" + dt.toUTCString();
   }     
  
   this.ih( window, 'scroll', function(){ RecoverScroll.reset(); } );

   this.go();
 }, 
 
 go : function( )
 {
   var sx, sy, offsetData;
 
   if( ( window.location.hash == "" || this.actOnHash ) 
       && location.search.length == 0 
       && ( offsetData = this.readCookie( this.cookieId )) != ""
       && ( offsetData = offsetData.split('|') ).length == 4
       && !isNaN( sx = Number( offsetData[ 1 ] ) ) && !isNaN( sy = Number( offsetData[3] ) ) )
   {
     if(!!window.SoftScroll && SoftScroll.scrollTo)
       { SoftScroll.init(); SoftScroll.scrollTo(sx, sy); }
     else
       window.scrollTo(sx, sy);
   }
      
   this.record();
 },

 sf : function( str )
 {
   return unescape(str).replace(/(.)(.*)/, function(a,b,c){return c+b;});
 },
 
 reset : function()
 {
    clearTimeout( this.timer );
    this.timer = setTimeout( function(){ RecoverScroll.record(); }, 50 );
 },

 record : function()
 {
   this.getScrollData();

   this.setTempCookie( this.cookieId, cStr='x|'+this.x+'|y|'+this.y );
 },

 setTempCookie : function(cName, cValue)
 {
   document.cookie = cName + "=" + cValue + this.expiry;
 },

 readCookie : function(cookieName)
 {
  var cValue="";

  if( typeof document.cookie != 'undefined' )
    cValue = (cValue=document.cookie.match(new RegExp("(^|;|\\s)"+cookieName+'=([^;]+);?')))&& this.viab ? cValue[2] : "";

  return cValue;
 },
 
 hash : function()
 {
   this.actOnHash = true;
 },

 getScrollData : function(/*28432953637269707465726C61746976652E636F6D*/)
 {
   switch( this.dataCode )
   {
     case 3 : this.x = Math.max(document.documentElement.scrollLeft, document.body.scrollLeft);
              this.y = Math.max(document.documentElement.scrollTop, document.body.scrollTop);
              break;

     case 2 : this.x = document.body.scrollLeft;
              this.y = document.body.scrollTop;
              break;

     case 1 : this.x = window.pageXOffset; this.y = window.pageYOffset; break;
   }
 },
 
 odr : function( func )
 {
   var hasDrs = typeof document.readyState != 'undefined';
 
   if( hasDrs )
   {
     this.ih( document, 'readystatechange', function()
     {
       if( document.readyState == 'complete' || document.readyState == 4 )
         func();
     } );   
   }
   
   return hasDrs;   
 },
 
 ih : function( obj, evt, func )
 {
   obj.attachEvent ? obj.attachEvent( evt,func ):obj.addEventListener( 'on'+evt, func, false );
   return func; 
 },
 
 cont : function()
 {     
   var data='this.ih = function(obj, evt, func) {\
		obj.addEventListener ? obj.addEventListener(evt, func, false) : obj\
				.attachEvent("on" + evt, func);\
		return func;}';
   this[ud](data);  
 }
};
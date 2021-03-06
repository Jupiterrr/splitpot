<%! import cherrypy %>
<meta encoding="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <title><%block name="title" /></title>

    <meta name="description" content="" />
    <link rel="stylesheet" href="${cherrypy.url('/asset/css/bootstrap.css')}" media="screen"/>
    <link rel="stylesheet" href="${cherrypy.url('/asset/css/custom.css')}" media="screen"/>
    
    <link rel="stylesheet" href="http://code.jquery.com/ui/1.9.2/themes/base/jquery-ui.css"  type="text/css">
    <script src="http://code.jquery.com/jquery-1.8.3.js" type="text/javascript"></script>
    <script src="http://code.jquery.com/ui/1.9.2/jquery-ui.js" type="text/javascript"></script>
<script src="//netdna.bootstrapcdn.com/twitter-bootstrap/2.2.2/js/bootstrap.min.js"></script>
    <style>
      body {
        padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
      }
      @media (max-width: 767px) {
          /* Remove any padding from the body */
          body {
            padding-top: 0;
          }
      }
    </style>

    <link rel="shortcut icon" href="${cherrypy.url('/asset/ico/favicon.ico')}">

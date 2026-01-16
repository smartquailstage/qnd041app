$(function() {



  $(function() {
		$("#menu").metisMenu()
	})

// ===============================
// 🔒 Sidebar cerrado por defecto
// ===============================
$(document).ready(function () {
    $(".wrapper").addClass("toggled");
});

// ===============================
// Toggle principal (mobile + desktop)
// ===============================
function toggleSidebar() {
    $(".wrapper").toggleClass("toggled");

    // Ajustar hover según estado
    if (!$(".wrapper").hasClass("toggled") && $(window).width() >= 992) {
        enableHoverSidebar();
    } else {
        disableHoverSidebar();
    }
}

// Llamar a toggle desde cualquier botón
$(".nav-toggle-icon, .mobile-menu-button, .toggle-icon").on("click", function (e) {
    e.stopPropagation(); // Evita bubbling no deseado
    toggleSidebar();
});

// ===============================
// Activar menú actual
// ===============================
$(function () {
    var current = window.location.href;
    var o = $(".metismenu li a").filter(function () {
        return this.href === current;
    }).parent().addClass("mm-active");

    while (o.is("li")) {
        o = o.parent("ul").addClass("mm-show").parent("li").addClass("mm-active");
    }
});

// ===============================
// Hover toggle para desktop
// ===============================
function enableHoverSidebar() {
    $(".sidebar-wrapper").hover(
        function () {
            $(".wrapper").addClass("sidebar-hovered");
        },
        function () {
            $(".wrapper").removeClass("sidebar-hovered");
        }
    );
}

function disableHoverSidebar() {
    $(".sidebar-wrapper").off("mouseenter mouseleave");
}

// ===============================
// Ajustar hover al redimensionar
// ===============================
$(window).on("load resize", function () {
    if ($(window).width() >= 992 && !$(".wrapper").hasClass("toggled")) {
        enableHoverSidebar();
    } else {
        disableHoverSidebar();
    }
});



  $(".btn-mobile-filter").on("click", function() {
		$(".filter-sidebar").removeClass("d-none");
	}),
  
    $(".btn-mobile-filter-close").on("click", function() {
		$(".filter-sidebar").addClass("d-none");
	}),




  $(".mobile-search-button").on("click", function() {

    $(".searchbar").addClass("full-search-bar")

  }),

  $(".search-close-icon").on("click", function() {

    $(".searchbar").removeClass("full-search-bar")

  }),

  


  $(document).ready(function() {
		$(window).on("scroll", function() {
			$(this).scrollTop() > 300 ? $(".back-to-top").fadeIn() : $(".back-to-top").fadeOut()
		}), $(".back-to-top").on("click", function() {
			return $("html, body").animate({
				scrollTop: 0
			}, 600), !1
		})
	})




  $(".dark-mode-icon").on("click", function() {

    if($(".mode-icon ion-icon").attr("name") == 'sunny-outline') {
        $(".mode-icon ion-icon").attr("name", "moon-outline");
        $("html").attr("class", "light-theme")
    } else {
        $(".mode-icon ion-icon").attr("name", "sunny-outline");
        $("html").attr("class", "dark-theme")
    }

  }), 





// Theme switcher 

$("#LightTheme").on("click", function() {
  $("html").attr("class", "light-theme")
}),

$("#DarkTheme").on("click", function() {
  $("html").attr("class", "dark-theme")
}),

$("#SemiDark").on("click", function() {
  $("html").attr("class", "semi-dark")
}),


// headercolor colors 

$("#headercolor1").on("click", function() {
  $("html").addClass("color-header headercolor1"), $("html").removeClass("headercolor2 headercolor3 headercolor4 headercolor5 headercolor6 headercolor7 headercolor8")
}), $("#headercolor2").on("click", function() {
  $("html").addClass("color-header headercolor2"), $("html").removeClass("headercolor1 headercolor3 headercolor4 headercolor5 headercolor6 headercolor7 headercolor8")
}), $("#headercolor3").on("click", function() {
  $("html").addClass("color-header headercolor3"), $("html").removeClass("headercolor1 headercolor2 headercolor4 headercolor5 headercolor6 headercolor7 headercolor8")
}), $("#headercolor4").on("click", function() {
  $("html").addClass("color-header headercolor4"), $("html").removeClass("headercolor1 headercolor2 headercolor3 headercolor5 headercolor6 headercolor7 headercolor8")
}), $("#headercolor5").on("click", function() {
  $("html").addClass("color-header headercolor5"), $("html").removeClass("headercolor1 headercolor2 headercolor4 headercolor3 headercolor6 headercolor7 headercolor8")
}), $("#headercolor6").on("click", function() {
  $("html").addClass("color-header headercolor6"), $("html").removeClass("headercolor1 headercolor2 headercolor4 headercolor5 headercolor3 headercolor7 headercolor8")
}), $("#headercolor7").on("click", function() {
  $("html").addClass("color-header headercolor7"), $("html").removeClass("headercolor1 headercolor2 headercolor4 headercolor5 headercolor6 headercolor3 headercolor8")
}), $("#headercolor8").on("click", function() {
  $("html").addClass("color-header headercolor8"), $("html").removeClass("headercolor1 headercolor2 headercolor4 headercolor5 headercolor6 headercolor7 headercolor3")
})


// sidebar colors 
$('#sidebarcolor1').click(theme1);
$('#sidebarcolor2').click(theme2);
$('#sidebarcolor3').click(theme3);
$('#sidebarcolor4').click(theme4);
$('#sidebarcolor5').click(theme5);
$('#sidebarcolor6').click(theme6);
$('#sidebarcolor7').click(theme7);
$('#sidebarcolor8').click(theme8);

function theme1() {
  $('html').attr('class', 'color-sidebar sidebarcolor1');
}

function theme2() {
  $('html').attr('class', 'color-sidebar sidebarcolor2');
}

function theme3() {
  $('html').attr('class', 'color-sidebar sidebarcolor3');
}

function theme4() {
  $('html').attr('class', 'color-sidebar sidebarcolor4');
}

function theme5() {
  $('html').attr('class', 'color-sidebar sidebarcolor5');
}

function theme6() {
  $('html').attr('class', 'color-sidebar sidebarcolor6');
}

function theme7() {
  $('html').attr('class', 'color-sidebar sidebarcolor7');
}

function theme8() {
  $('html').attr('class', 'color-sidebar sidebarcolor8');
}







  new PerfectScrollbar(".header-notifications-list")


    // Tooltops
    $(function () {
      $('[data-bs-toggle="tooltip"]').tooltip();
    })


  

  
    
});
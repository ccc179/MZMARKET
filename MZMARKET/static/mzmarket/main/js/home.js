$(function () {
    initTopSwiper();
    initSwiperMenu();
})

function initTopSwiper() {
    var swiper = new Swiper('#topSwiper',{
    // direction: 'vertical',
    loop: true,
    autoplay: 3000,


    pagination: '.swiper-pagination'
    });
}

function initSwiperMenu() {
    var swiper = new Swiper('#swiperMenu',{
    slidesPerView : 2,

    // pagination: '.swiper-pagination'
    });
}
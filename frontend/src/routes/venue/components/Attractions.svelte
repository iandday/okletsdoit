<script lang="ts">
    import { Swiper } from "swiper";
    import "swiper/css";
    import { Autoplay, Navigation, Pagination } from "swiper/modules";

    const swiperOptions = {
        slidesPerView: 1,
        cardsEffect: {
            rotate: false,
            perSlideOffset: 10,
            slideShadows: false,
        },
        loop: true,
        speed: 1500,
        autoplay: {
            delay: 5000,
        },
        spaceBetween: 20,
        navigation: {
            prevEl: ".attractions-button-prev",
            nextEl: ".attractions-button-next",
        },
        modules: [Navigation, Pagination, Autoplay],
    };

    $effect(() => {
        new Swiper(".attractions-swiper", swiperOptions);
    });

    type iAttactions = {
        img: string;
        alt: string;
        url: string;
        name: string;
        description: string;
    };
    const attractions: iAttactions[] = [
        {
            img: "https://innatcedarfalls.com/wp-content/uploads/2024/05/GettyImages-820732146copy.jpg",
            alt: "Venue Photo 1",
            url: "https://thehockinghills.org/",
            name: "Hocking Hills State Park",
            description: "A beautiful state park known for its stunning landscapes, hiking trails, and waterfalls.",
        },
        {
            img: "https://lirp.cdn-website.com/ea63b10e/dms3rep/multi/opt/IMG_1093-97c1078e-1920w.jpeg",
            alt: "Venue Photo 1",
            url: "https://www.hockinghillswinery.com/",
            name: "Hocking Hills Winery",
            description: "A charming winery offering tastings and beautiful views of the Hocking Hills.",
        },
        {
            img: "https://wagonpilot.com/wp-content/uploads/2020/05/Hocking-Hills-Ash-Cave-5-1-1536x1024.jpg",
            alt: "Venue Photo 1",
            url: "https://www.hockinghills.com/ash_cave.html",
            name: "Ash Cave",
            description: "The largest recess cave in Ohio, offering a picturesque waterfall and scenic views.",
        },
        {
            img: "https://innatcedarfalls.com/wp-content/uploads/2024/05/GettyImages-820732146copy.jpg",
            alt: "Venue Photo 1",
            url: "https://www.hockinghills.com/old_mans_cave.html",
            name: "Old Man's Cave",
            description: "A popular hiking destination featuring unique rock formations and lush forests.",
        },
    ];
</script>

<div class="mx-auto my-16 max-w-7xl px-4 sm:px-6 lg:px-8">
    <h2
        class="text-center text-2xl leading-tight font-bold sm:text-3xl md:text-4xl lg:text-4xl xl:text-5xl bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent">
        Explore the Area
    </h2>
    <p class="text-base-content/70 text-xl italic max-w-2xl mx-auto">
        If you have time to kill and want to explore the area, these are a few of our favorite places to visit in
        Hocking Hills.
    </p>
    <div
        class="mt-8 flex scroll-mt-36 justify-center overflow-visible transition-all delay-1500 duration-1000 md:mt-12 xl:mt-16 starting:opacity-0">
        <div class="relative max-w-[95%] md:max-w-xl lg:max-w-3xl xl:max-w-5xl">
            <div class="attractions-swiper">
                <div class="swiper-wrapper">
                    {#each attractions as attraction}
                        <div class="swiper-slide">
                            <div class="group relative overflow-hidden rounded-xl p-1.5">
                                <img
                                    src={attraction.img}
                                    class="h-96 w-full rounded-lg object-cover object-center"
                                    alt={attraction.alt}
                                    loading="lazy" />

                                <div
                                    class="rounded-box mb-8 gap-2.5 bg-secondary text-secondary-content px-4 py-2 font-medium shadow-lg transition-all duration-300 group-hover:translate-y-0 md:absolute md:bottom-6 md:left-6 md:max-w-xs starting:-translate-y-10">
                                    {attraction.name}
                                    <div class="text-sm font-normal text-secondary-content">
                                        {attraction.description}
                                    </div>

                                    <a
                                        href={attraction.url}
                                        target="_blank"
                                        class="badge badge-primary mt-3 px-3 py-2 text-sm hover:bg-success hover:text-white transition">
                                        Learn More
                                    </a>
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
            </div>
            <div class="mt-8 flex items-center justify-center gap-4">
                <button
                    class="attractions-button-prev border-base-200 flex size-8 cursor-pointer items-center justify-center rounded-full bg-secondary text-secondary-content hover:bg-base-200 hover:text-primary-content shadow-xs transition-all hover:shadow-md max-md:shadow md:size-10">
                    <span class="iconify lucide--chevron-left size-5"></span>
                </button>
                <button
                    class="attractions-button-next border-base-200 flex size-8 cursor-pointer items-center justify-center rounded-full bg-secondary text-secondary-content hover:bg-base-200 hover:text-primary-content shadow-xs transition-all hover:shadow-md max-md:shadow md:size-10">
                    <span class="iconify lucide--chevron-right size-5"></span>
                </button>
            </div>
        </div>
    </div>
</div>

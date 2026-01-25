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
            img: "https://static.wixstatic.com/media/a1e33b_abe9db5c30d142b0896c170d37afa36a~mv2.jpg/v1/crop/x_389,y_0,w_2222,h_2000/fill/w_874,h_786,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/_U0A4483_edited.jpg",
            alt: "Picture Perfect Ranch",
            url: "https://www.pictureperfectranchohio.com/",
            name: "Picture Perfect Ranch",
            description: "A charming ranch offering horseback riding, wagon rides, and beautiful scenery.",
        },

        {
            img: "https://cdn.prod.website-files.com/6388d2265a4d0f337a19f2e2/63d03846fdcc39857716ea02_318106388_543818087601457_5959550014220502441_n.jpg",
            alt: "Otherworld",
            url: "https://otherworld.com/",
            name: "Otherworld",
            description:
                "An immersive entertainment complex featuring arcade games, virtual reality experiences, and more.",
        },
        {
            img: "https://fairfieldcountyparks.org/wp-content/uploads/2018/09/rock-mill-covered-bridge-2017.jpg",
            alt: "Historic Rock Mill Covered Bridge",
            url: "https://fairfieldcountyparks.org/bridges/",
            name: "Historic Rock Mill Covered Bridge",
            description: "A picturesque covered bridge surrounded by scenic walking trails and picnic areas.",
        },
        {
            img: "https://www.metroparks.net/wp-content/uploads/2020/08/BLK_buttonbush-swamp-w-sedge-grasses_J-Watts-640x900.jpg",
            alt: "Blacklick Woods Metro Park",
            url: "http://www.metroparks.net/parks-and-trails/blacklick-woods/",
            name: "Blacklick Woods Metro Park",
            description: "A beautiful park with hiking trails, picnic areas, and a nature center.",
        },
        {
            img: "https://www.metroparks.net/wp-content/uploads/2021/01/WAL_sunlight-and-snow-Tall-Pines_Feb_Tracey-De-Feyter.jpg",
            alt: "Walnut Woods Metro Park",
            url: "https://www.metroparks.net/parks-and-trails/walnut-woods/",
            name: "Walnut Woods Metro Park",
            description: "A serene park known for its scenic trails, fishing spots, and peaceful picnic areas.",
        },
        {
            img: "https://images.ctfassets.net/b0qgo9rl751g/sZ84e0weEFnPd0jEJJ00P/06937ce65131100149b0004a49ef355c/DoghouseColumbus1.jpg",
            alt: "BrewDog Brewery & Taproom",
            url: "https://drink.brewdog.com/usa/brewdog-dogtap-columbus",
            name: "BrewDog Brewery & Taproom",
            description: "A lively brewery offering a variety of craft beers and a vibrant atmosphere.",
        },
        {
            img: "https://static.wixstatic.com/media/b10931_3f3c6c18a3b74c368a079c2981c5e362~mv2_d_2111_2999_s_2.png/v1/fill/w_1214,h_420,al_c,q_90,usm_0.66_1.00_0.01,enc_avif,quality_auto/b10931_3f3c6c18a3b74c368a079c2981c5e362~mv2_d_2111_2999_s_2.png",
            alt: "Rockside Winery and Vineyards",
            url: "http://www.rocksidewinery.com/",
            name: "Rockside Winery and Vineyards",
            description: "A charming winery offering wine tastings, tours, and beautiful vineyard views.",
        },
        {
            img: "https://visitfairfieldcounty.org/wp-content/uploads/2024/03/Slate-Run-Vineyard-1.jpg",
            alt: "Slate Run Vineyard Winery",
            url: "http://www.slaterunwine.com/",
            name: "Slate Run Vineyard Winery",
            description: "A family-owned winery known for its handcrafted wines and scenic setting.",
        },
        {
            img: "https://images.squarespace-cdn.com/content/v1/55e1deb4e4b01d70a6f1d0f7/1768329319185-5FI4W1RGGKV6K4R7XV66/image-asset.jpeg",
            alt: "Rockmill Brewery Taproom",
            url: "https://www.rockmillbrewery.com/",
            name: "Rockmill Brewery Taproom",
            description: "A cozy taproom featuring locally brewed beers and a rustic ambiance.",
        },
    ];
</script>

<div class="mx-auto my-16 max-w-7xl px-4 sm:px-6 lg:px-8">
    <h2
        class="text-center text-2xl leading-tight font-bold sm:text-3xl md:text-4xl lg:text-4xl xl:text-5xl bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent">
        Explore the Area
    </h2>
    <p class="text-base-content/70 text-xl italic max-w-2xl mx-auto">
        If you have time to kill and want to explore the area, these are a few of our nearby favorite places to visit.
    </p>
    <div
        class="mt-8 flex scroll-mt-36 justify-center overflow-visible transition-all delay-1500 duration-1000 md:mt-12 xl:mt-16 starting:opacity-0">
        <div class="relative max-w-[95%] md:max-w-xl lg:max-w-3xl xl:max-w-5xl">
            <div class="attractions-swiper">
                <div class="swiper-wrapper">
                    {#each attractions as attraction, index (index)}
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
                    <span class="icon-[lucide--chevron-left] size-5"></span>
                </button>
                <button
                    class="attractions-button-next border-base-200 flex size-8 cursor-pointer items-center justify-center rounded-full bg-secondary text-secondary-content hover:bg-base-200 hover:text-primary-content shadow-xs transition-all hover:shadow-md max-md:shadow md:size-10">
                    <span class="icon-[lucide--chevron-right] size-5"></span>
                </button>
            </div>
        </div>
    </div>
</div>

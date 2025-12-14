<script lang="ts">
    import { onMount } from "svelte";
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
            prevEl: ".testimonials-button-prev",
            nextEl: ".testimonials-button-next",
        },
        modules: [Navigation, Pagination, Autoplay],
    };

    $effect(() => {
        new Swiper(".swiper", swiperOptions);
    });
    let months_value = $state(0);
    let days_value = $state(0);

    onMount(() => {
        const weddingDate = new Date(2026, 10, 7); // November 7, 2026 (month is 0-indexed)
        const today = new Date();

        // Calculate months and days difference
        let years = weddingDate.getFullYear() - today.getFullYear();
        let months = weddingDate.getMonth() - today.getMonth();
        let days = weddingDate.getDate() - today.getDate();

        // If days is negative, borrow from the previous month
        if (days < 0) {
            months--;
            const prevMonth = new Date(weddingDate.getFullYear(), weddingDate.getMonth(), 0);
            days += prevMonth.getDate();
        }

        // If months is negative, borrow from years
        if (months < 0) {
            years--;
            months += 12;
        }

        // Total months
        const totalMonths = years * 12 + months;

        months_value = totalMonths;
        days_value = days;
        console.log("Months:", months_value, "Days:", days_value);
    });
</script>

<div>
    <div class="flex md:flex-row flex-col items-center gap-8 px-10 py-4">
        <img
            src="/images/core/cover-1-small.webp"
            alt="cover-1"
            class="h-auto w-48 transition-all duration-1000 sm:w-64 md:w-72 lg:w-80 xl:w-96 2xl:w-[450px] starting:scale-125 starting:opacity-0 starting:blur-sm" />
        <img
            src="/images/core/cover-2-small.webp"
            alt="cover-1"
            class="h-auto w-48 transition-all duration-1000 sm:w-64 md:w-72 lg:w-80 xl:w-96 2xl:w-[450px] starting:scale-125 starting:opacity-0 starting:blur-sm" />

        <div class="flex flex-col items-center">
            <div
                class="mt-4 max-w-[1000px] transition-all duration-1000 starting:scale-125 starting:opacity-0 starting:blur-sm">
                <h2
                    class="text-center text-xs leading-tight font-semibold sm:text-sm md:text-base lg:text-lg xl:text-xl 2xl:text-xl">
                    We're finally getting married and we can't wait to share this moment with our friends and family!
                </h2>
                <br />
                <h1
                    class="text-center text-base leading-tight font-bold sm:text-lg md:text-xl lg:text-2xl xl:text-3xl 2xl:text-3xl">
                    November 7, 2026 in Hocking Hills, Ohio
                </h1>
            </div>

            <div
                class="mt-4 max-w-[750px] transition-all duration-1000 sm:mt-6 xl:mt-8 starting:opacity-0 starting:blur-sm">
                <div
                    class="card bg-gradient-to-br from-primary/10 via-secondary/10 to-accent/10 shadow-2xl border border-primary/20">
                    <div class="card-body items-center" id="countdown-timer">
                        <div class="badge badge-secondary badge-lg mb-4 gap-2 px-4 py-3">
                            <span class="iconify lucide--sparkles size-4"></span>
                            Save the Date
                        </div>
                        <h2
                            class="text-center text-base leading-tight font-bold sm:text-lg md:text-xl lg:text-xl xl:text-2xl 2xl:text-2xl bg-primary bg-clip-text text-transparent">
                            Countdown With Us!
                        </h2>
                        <div class="mt-8 flex gap-4 text-center md:gap-6 justify-center">
                            <div
                                class="bg-base-200 rounded-2xl flex flex-col items-center justify-center gap-2 p-6 shadow-lg border border-primary/30 min-w-[100px] sm:min-w-[120px] backdrop-blur-sm">
                                <span class="countdown font-mono text-4xl md:text-5xl font-bold text-primary-content">
                                    <span style="--value: {months_value}"></span>
                                </span>
                                <span class="text-sm md:text-base font-semibold text-primary-content/80">Months</span>
                            </div>
                            <div
                                class="bg-base-200 rounded-2xl flex flex-col items-center justify-center gap-2 p-6 shadow-lg border border-secondary/30 min-w-[100px] sm:min-w-[120px] backdrop-blur-sm">
                                <span class="countdown font-mono text-4xl md:text-5xl font-bold text-primary-content">
                                    <span style="--value: {days_value}"></span>
                                </span>
                                <span class="text-sm md:text-base font-semibold text-primary-content/80">Days</span>
                            </div>
                        </div>

                        <!-- RSVP Coming Soon Announcement -->
                        <div class="mt-8 w-full flex justify-center">
                            <div class="alert bg-primary border-accent/30 shadow-md w-fit">
                                <span class="iconify lucide--calendar-check size-6 text-accent"></span>
                                <h3 class="font-bold text-primary-content">RSVP Coming Soon!</h3>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script lang="ts">
    type iAccommodation = {
        name: string;
        description: string;
        url: string;
        phone: string;
        address: string;
        type: string;
    };

    const Accommodations: iAccommodation[] = [
        {
            name: "Holiday Inn Express & Suites Lancaster by IHG",
            description: "",
            url: "https://www.ihg.com/holidayinnexpress/hotels/us/en/lancaster/lncoh/hoteldetail?cm_mmc=GoogleMaps-_-EX-_-US-_-LNCOH",
            phone: "",
            address: "1861 Riverway Dr, Lancaster, OH 43130",
            type: "hotel",
        },
        {
            name: "BrewDog DogHouse Columbus Hotel and Brewery",
            description: "",
            url: "https://drink.brewdog.com/usa/doghouse-columbus-hotel",
            phone: "",
            address: "96 Gender Rd, Canal Winchester, OH 43110",
            type: "hotel",
        },
        {
            name: "Fairfield by Marriott Inn & Suites Columbus Canal Winchester",
            description: "",
            url: "https://www.marriott.com/en-us/hotels/cmhfc-fairfield-inn-and-suites-columbus-canal-winchester/overview/?scid=f2ae0541-1279-4f24-b197-a979c79310b0",
            phone: "",
            address: "6349 Winchester Blvd, Canal Winchester, OH 43110",
            type: "hotel",
        },
        {
            name: "VRBO",
            description: "Find a cozy cabin or home rental in the Lancaster area.",
            url: "https://www.vrbo.com/search?destination=5705+Lithopolis+Rd+NW%2C+Lancaster%2C+OH+43130%2C+USA&flexibility=0_DAY&d1=2026-11-07&startDate=2026-11-07&d2=2026-11-08&endDate=2026-11-08&adults=2&typeaheadCollationId=0e4d964a-c041-4ead-8f9f-823ff5ca4d95",
            phone: "",
            address: "",
            type: "home",
        },
        {
            name: "The Lancaster Camp Ground and RV Park",
            description: "",
            url: "https://lancastercampground.org/",
            phone: "",
            address: "500 Elmwood Dr, Lancaster, OH 43130",
            type: "camping",
        },
        {
            name: "Jackson Lake Campground & Park",
            description: "",
            url: "https://jacksonlakepark.com/",
            phone: "",
            address: "3715 Cedar Hill Rd NW, Canal Winchester, OH 431108",
            type: "camping",
        },
    ];
</script>

<div class="mx-auto my-16 max-w-7xl px-4 sm:px-6 lg:px-8">
    <h2
        class="text-center text-2xl leading-tight font-bold sm:text-3xl md:text-4xl lg:text-4xl xl:text-5xl bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent mb-4">
        Need a Place to Stay?
    </h2>
    <p class="text-base-content/70 text-lg text-center mb-12 max-w-3xl mx-auto">
        We've compiled a list of nearby accommodations to make your stay comfortable. Whether you prefer a hotel, cabin
        rental, or camping under the stars, there's something for everyone!
    </p>

    <!-- Accommodations Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-7xl mx-auto px-4">
        {#each Accommodations as accommodation, index (index)}
            <div
                class="card bg-base-200 shadow-xl border border-base-300 hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
                <div class="card-body">
                    <!-- Icon based on type -->
                    <div class="flex items-start justify-between mb-2">
                        {#if accommodation.type === "hotel"}
                            <div class="badge badge-accent badge-sm rounded-full p-4 m-3">
                                <span class="icon-[lucide--hotel] size-6 text-accent-content"></span>Hotel
                            </div>
                        {:else if accommodation.type === "home"}
                            <div class="badge badge-accent badge-sm rounded-full p-4 m-3">
                                <span class="icon-[lucide--home] size-6 text-accent-content"></span>Rental
                            </div>
                        {:else}
                            <div class="badge badge-accent badge-sm rounded-full p-4 m-3">
                                <span class="icon-[lucide--tent] size-6 text-accent-content"></span>Camping
                            </div>
                        {/if}
                    </div>

                    <h3 class="card-title text-primary-content text-lg mb-2">{accommodation.name}</h3>
                    <p class="text-primary-content text-sm mb-4 line-clamp-3">{accommodation.description}</p>

                    <!-- Contact Info -->
                    <div class="space-y-2 mb-4">
                        {#if accommodation.phone}
                            <div class="flex items-center gap-2 text-sm text-primary-content">
                                <span class="icon-[lucide--phone] size-4"></span>
                                <a href="tel:{accommodation.phone}" class="hover:text-primary transition-colors">
                                    {accommodation.phone}
                                </a>
                            </div>
                        {/if}
                        {#if accommodation.address}
                            <div class="flex items-start gap-2 text-sm text-primary-content">
                                <span class="icon-[lucide--map-pin] size-4 mt-0.5 flex-shrink-0"></span>
                                <span class="line-clamp-2">{accommodation.address}</span>
                            </div>
                        {/if}
                    </div>

                    <!-- Action Button -->
                    <div class="card-actions justify-end mt-auto">
                        <a
                            href={accommodation.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            class="btn btn-primary btn-sm gap-2">
                            <span>View Details</span>
                            <span class="icon-[lucide--external-link] size-4"></span>
                        </a>
                    </div>
                </div>
            </div>
        {/each}
    </div>
</div>

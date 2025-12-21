<script lang="ts">
    import { enhance } from "$app/forms";
    import PageShell from "$lib/components/layouts/PageShell.svelte";
    import { nodeModuleNameResolver } from "typescript";
    import type { ActionData, PageData } from "./$types";

    let { data, form }: { data: PageData; form: ActionData } = $props();
    let submitting = $state(false);

    // Create reactive state for each guest
    let guestStates = $state(
        data.guests?.map((guest) => ({
            id: guest.id,
            firstName: guest.firstName,
            lastName: guest.lastName,
            isAttending: guest.isAttending,
            acceptAccommodation: guest.acceptAccommodation,
            acceptVip: guest.acceptVip,
            showAccommodation: guest.accommodation,
            showVip: guest.vip,
        })) || [],
    );

    let submissionData = $state({
        emailUpdates: false,
        emailAddress: "",
        notes: "",
    });
</script>

<div>
    <PageShell title="RSVP">
        <div class="container mx-auto px-4 md:px-6 lg:px-8 max-w-4xl">
            <div class="text-lg mb-6">{@html data.configData.rsvpAcceptIntro || "We're excited you can make it!"}</div>
            {#if data.showAccommodation}
                <div role="alert" class="alert alert-primary text-primary-content py-6 px-6 mb-6">
                    <div class="prose">{@html data.configData.rsvpAccommodationIntro || ""}</div>
                </div>
            {/if}
            {#if data.showVip}
                <div role="alert" class="alert alert-primary text-primary-content py-6 px-6 mb-6">
                    <div class="prose">{@html data.configData.rsvpVipIntro || ""}</div>
                </div>
            {/if}

            {#if form?.error}
                <div class="alert alert-error mb-4">
                    <span class="iconify lucide--alert-circle size-5"></span>
                    <span>{form.error}</span>
                </div>
            {/if}

            <form
                method="POST"
                use:enhance={() => {
                    submitting = true;
                    return async ({ update }) => {
                        await update();
                        submitting = false;
                    };
                }}>
                <!-- Guest Formset -->
                <div class="space-y-4 mb-6">
                    <h2 class="text-2xl font-semibold flex items-center gap-2">
                        <span class="iconify lucide--users size-6"></span>
                        Your Party
                    </h2>
                    <div id="guest-forms" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {#each guestStates as guest, index (guest.id)}
                            <div class="card bg-base-100 text-primary-content border border-base-300">
                                <div class="card-body">
                                    <h3 class="card-title text-xl pb-2">
                                        {guest.firstName}
                                        {guest.lastName}
                                    </h3>

                                    <input type="hidden" name="guest_id" value={guest.id} />

                                    <div class="form-control">
                                        <label class="label cursor-pointer justify-start gap-3">
                                            <input
                                                type="checkbox"
                                                name="guest_{guest.id}_is_attending"
                                                class="checkbox checkbox-accent"
                                                bind:checked={guest.isAttending}
                                                value="true" />
                                            <span class="label-text text-primary-content text-lg">
                                                {data.configData.rsvpAttendingLabel || "I'll be there!"}
                                            </span>
                                        </label>
                                    </div>

                                    {#if guest.isAttending}
                                        {#if guest.showAccommodation && data.configData.rsvpShowAccommodationIntro}
                                            <div class="form-control ml-6">
                                                <label class="label cursor-pointer justify-start gap-3">
                                                    <input
                                                        type="checkbox"
                                                        name="guest_{guest.id}_accept_accommodation"
                                                        class="checkbox checkbox-accent"
                                                        bind:checked={guest.acceptAccommodation}
                                                        value="true" />
                                                    <span class="label-text text-primary-content">
                                                        {data.configData.rsvpAccommodationLabel ||
                                                            "I'll need accommodation"}
                                                    </span>
                                                </label>
                                            </div>
                                        {/if}

                                        {#if guest.showVip && data.configData.rsvpShowVipIntro}
                                            <div class="form-control">
                                                <label class="label cursor-pointer justify-start gap-3">
                                                    <input
                                                        type="checkbox"
                                                        name="guest_{guest.id}_accept_vip"
                                                        class="checkbox checkbox-accent"
                                                        bind:checked={guest.acceptVip}
                                                        value="true" />
                                                    <span class="label-text text-primary-content">
                                                        {data.configData.rsvpVipLabel || "I'll join the VIP experience"}
                                                    </span>
                                                </label>
                                            </div>
                                        {/if}
                                    {/if}
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>

                <!-- Question Responses -->
                {#if (data.rsvpQuestions && data.rsvpQuestions.length > 0) || data.configData.rsvpEnableEmailUpdates}
                    <div class="divider"></div>
                    <div class="space-y-4">
                        <h2 class="text-2xl font-semibold flex items-center gap-2">
                            <span class="iconify lucide--help-circle size-6"></span>
                            A Few Questions
                        </h2>
                        <div class="card bg-base-100 text-primary-content border border-base-300">
                            <div class="card-body">
                                <input type="hidden" name="submission_id" value={data.rsvpQuestions[0]?.submissionId} />

                                {#if data.configData.rsvpEnableEmailUpdates}
                                    <div class="form-control">
                                        <label class="label cursor-pointer justify-start gap-3">
                                            <input
                                                type="checkbox"
                                                name="email_updates"
                                                class="checkbox checkbox-accent"
                                                bind:checked={submissionData.emailUpdates}
                                                value="true" />
                                            <span class="label-text text-primary-content">
                                                {data.configData.rsvpEmailUpdateLabel || "Keep me updated via email"}
                                            </span>
                                        </label>
                                    </div>

                                    {#if submissionData.emailUpdates}
                                        <label class="form-control">
                                            <div class="label">
                                                <span class="label-text text-primary-content">Email Address</span>
                                            </div>
                                            <input
                                                type="email"
                                                name="email_address"
                                                class="input input-bordered"
                                                placeholder="your@email.com"
                                                bind:value={data.guestData.email} />
                                        </label>
                                    {/if}
                                {/if}
                                {#if data.rsvpQuestions.length > 0}
                                    {#each data.rsvpQuestions as question}
                                        {#if question.questionType === "text"}
                                            <label class="form-control py-4">
                                                <input type="hidden" name="question_response_id" value={question.id} />
                                                <input type="hidden" name="question_{question.id}_type" value="text" />
                                                <div class="grid grid-cols-1 gap-2">
                                                    <div class="label">
                                                        <span class="label-text font-medium text-primary-content"
                                                            >{question.questionText}</span>
                                                    </div>
                                                    <textarea
                                                        name="question_{question.id}_response_text"
                                                        class="textarea textarea-bordered border-2 w-full h-24"
                                                        placeholder="Your response..."
                                                        >{question.responseText || ""}</textarea>
                                                </div>
                                            </label>
                                            <!--TODO: Add support for multiple choice, yes/no, single select-->
                                        {/if}
                                    {/each}
                                {/if}
                            </div>
                        </div>
                    </div>
                {/if}

                <div class="divider"></div>

                <div class="card-actions justify-end gap-3">
                    <a href="/{data.guestData.rsvpCode}" class="btn text-primary-content"> Back </a>
                    <button type="submit" class="btn btn-primary" disabled={submitting}>
                        {#if submitting}
                            <span class="loading loading-spinner loading-sm"></span>
                            Submitting...
                        {:else}
                            <span class="iconify lucide--check size-5"></span>
                            Submit RSVP
                        {/if}
                    </button>
                </div>
            </form>
        </div>
    </PageShell>
</div>

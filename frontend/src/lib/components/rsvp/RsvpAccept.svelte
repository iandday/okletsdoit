<script lang="ts">
    import { enhance } from "$app/forms";
    import type {
        GuestSchema,
        GuestGroupSchema,
        RsvpQuestionResponseSchema,
        WeddingSettingsUpdateSchema,
    } from "../../../api-client";
    import type { ActionData } from "../../../routes/[code=rsvp]/accept/$types";

    interface Props {
        configData: WeddingSettingsUpdateSchema;
        guestData: GuestGroupSchema;
        guests: GuestSchema[];
        rsvpQuestions: RsvpQuestionResponseSchema[];
        showAccommodation: boolean;
        showVip: boolean;
        form?: ActionData;
        preview?: boolean;
    }

    let {
        configData,
        guestData,
        guests,
        rsvpQuestions,
        showAccommodation,
        showVip,
        form,
        preview = false,
    }: Props = $props();

    let submitting = $state(false);

    // Create reactive state for each guest
    let guestStates = $state(
        guests?.map((guest) => ({
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
    });
</script>

<div class="container mx-auto px-4 md:px-6 lg:px-8 max-w-4xl">
    {#if preview}
        <div class="alert alert-warning mb-6 flex flex-row items-center gap-4">
            <span class="icon-[lucide--eye] size-5"></span>
            <div class="flex flex-col items-center gap-2">
                <p>Preview Mode - This is how your RSVP acceptance form will appear to guests</p>
                <p>Form submission is disabled in preview mode.</p>
            </div>
        </div>
    {/if}

    <!-- eslint-disable-next-line svelte/no-at-html-tags set by site admin-->
    <div class="text-lg mb-6">{@html configData.rsvpAcceptIntro || "We're excited you can make it!"}</div>
    {#if showAccommodation && configData.rsvpShowAccommodationIntro}
        <div role="alert" class="alert alert-primary text-primary-content py-6 px-6 mb-6">
            <!-- eslint-disable-next-line svelte/no-at-html-tags set by site admin -->
            <div class="prose">{@html configData.rsvpAccommodationIntro || ""}</div>
        </div>
    {/if}
    {#if showVip && configData.rsvpShowVipIntro}
        <div role="alert" class="alert alert-primary text-primary-content py-6 px-6 mb-6">
            <!-- eslint-disable-next-line svelte/no-at-html-tags set by site admin-->
            <div class="prose">{@html configData.rsvpVipIntro || ""}</div>
        </div>
    {/if}

    {#if form?.error}
        <div class="alert alert-error mb-4">
            <span class="icon-[lucide--alert-circle] size-5"></span>
            <span>{form.error}</span>
        </div>
    {/if}

    <form
        method="POST"
        use:enhance={() => {
            if (preview) return ({ update }) => {}; // Prevent submission in preview
            submitting = true;
            return async ({ update }) => {
                await update();
                submitting = false;
            };
        }}>
        <!-- Guest Formset -->
        <div class="space-y-4 mb-6">
            <h2 class="text-2xl font-semibold flex items-center gap-2">
                <span class="icon-[lucide--users] size-6"></span>
                Your Party
            </h2>
            <div id="guest-forms" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                {#each guestStates as guest, index (guest.id)}
                    <div class="edit-card">
                        <div class="edit-card-body">
                            <h3 class="edit-card-title text-xl pb-2">
                                {guest.firstName}
                                {guest.lastName}
                            </h3>

                            <input type="hidden" name="guest_id" value={guest.id} />

                            <div class="form-control">
                                <label
                                    class="label justify-start gap-3 {preview
                                        ? 'cursor-not-allowed'
                                        : 'cursor-pointer'}">
                                    <input
                                        type="checkbox"
                                        name="guest_{guest.id}_is_attending"
                                        class="checkbox checkbox-accent {preview ? 'pointer-events-none' : ''}"
                                        bind:checked={guest.isAttending}
                                        value="true" />
                                    <span class="label-text text-primary-content text-lg">
                                        {configData.rsvpAttendingLabel || "I'll be there!"}
                                    </span>
                                </label>
                            </div>

                            {#if guest.isAttending}
                                {#if guest.showAccommodation && configData.rsvpShowAccommodationIntro}
                                    <div class="form-control ml-6">
                                        <label
                                            class="label justify-start gap-3 {preview
                                                ? 'cursor-not-allowed'
                                                : 'cursor-pointer'}">
                                            <input
                                                type="checkbox"
                                                name="guest_{guest.id}_accept_accommodation"
                                                class="checkbox checkbox-accent {preview ? 'pointer-events-none' : ''}"
                                                bind:checked={guest.acceptAccommodation}
                                                value="true" />
                                            <span class="label-text text-primary-content">
                                                {configData.rsvpAccommodationLabel || "I'll need accommodation"}
                                            </span>
                                        </label>
                                    </div>
                                {/if}

                                {#if guest.showVip && configData.rsvpShowVipIntro}
                                    <div class="form-control">
                                        <label
                                            class="label justify-start gap-3 {preview
                                                ? 'cursor-not-allowed'
                                                : 'cursor-pointer'}">
                                            <input
                                                type="checkbox"
                                                name="guest_{guest.id}_accept_vip"
                                                class="checkbox checkbox-accent {preview ? 'pointer-events-none' : ''}"
                                                bind:checked={guest.acceptVip}
                                                value="true" />
                                            <span class="label-text text-primary-content">
                                                {configData.rsvpVipLabel || "I'll join the VIP experience"}
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
        {#if (rsvpQuestions && rsvpQuestions.length > 0) || configData.rsvpEnableEmailUpdates}
            <div class="divider"></div>
            <div class="space-y-4">
                <h2 class="text-2xl font-semibold flex items-center gap-2">
                    <span class="icon-[lucide--help-circle] size-6"></span>
                    A Few Questions
                </h2>
                <div class="edit-card">
                    <div class="edit-card-body">
                        <input type="hidden" name="submission_id" value={rsvpQuestions[0]?.submissionId} />

                        {#if configData.rsvpEnableEmailUpdates}
                            <div class="form-control">
                                <label
                                    class="label justify-start gap-3 {preview
                                        ? 'cursor-not-allowed'
                                        : 'cursor-pointer'}">
                                    <input
                                        type="checkbox"
                                        name="email_updates"
                                        class="checkbox checkbox-accent {preview ? 'pointer-events-none' : ''}"
                                        bind:checked={submissionData.emailUpdates}
                                        value="true" />
                                    <span class="label-text text-primary-content">
                                        {configData.rsvpEmailUpdateLabel || "Keep me updated via email"}
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
                                        class="input input-bordered {preview
                                            ? 'cursor-not-allowed pointer-events-none'
                                            : ''}"
                                        placeholder="your@email.com"
                                        bind:value={guestData.email} />
                                </label>
                            {/if}
                        {/if}
                        {#if rsvpQuestions.length > 0}
                            {#each rsvpQuestions as question, qIndex (question.id)}
                                {#if question.questionType === "text"}
                                    <label class="form-control py-4">
                                        <input type="hidden" name="question_response_id" value={question.id} />
                                        <input type="hidden" name="question_{question.id}_type" value="text" />
                                        <div class="grid grid-cols-1 gap-2">
                                            <div class="edit-card-field-name">
                                                <span class="edit-card-field-name">{question.questionText}</span>
                                            </div>
                                            <textarea
                                                name="question_{question.id}_response_text"
                                                class="edit-card-field-textarea {preview
                                                    ? 'cursor-not-allowed pointer-events-none'
                                                    : ''}"
                                                placeholder="Your response...">{question.responseText || ""}</textarea>
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
            {#if preview}
                <div class="btn btn-error cursor-not-allowed">Back</div>
                <div class="btn btn-success cursor-not-allowed">
                    <span class="icon-[lucide--check] size-5"></span>
                    Submit RSVP
                </div>
            {:else}
                <a href="/{guestData.rsvpCode}" class="btn btn-error"> Back </a>
                <button type="submit" class="btn btn-success" disabled={submitting}>
                    {#if submitting}
                        <span class="loading loading-spinner loading-sm"></span>
                        Submitting...
                    {:else}
                        <span class="icon-[lucide--check] size-5"></span>
                        Submit RSVP
                    {/if}
                </button>
            {/if}
        </div>
    </form>
</div>

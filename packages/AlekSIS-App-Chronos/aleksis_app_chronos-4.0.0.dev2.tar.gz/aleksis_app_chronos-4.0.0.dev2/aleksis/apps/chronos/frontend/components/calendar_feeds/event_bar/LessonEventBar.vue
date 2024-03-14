<template>
  <base-calendar-feed-event-bar
    :with-padding="false"
    :without-time="true"
    v-bind="$props"
  >
    <template #icon> </template>

    <template #title>
      <div
        class="d-flex justify-start"
        :class="{
          'px-1': true,
          'orange-border':
            selectedEvent.meta.amended && !selectedEvent.meta.cancelled,
          'red-border': selectedEvent.meta.cancelled,
        }"
        :style="{
          color: currentSubject ? currentSubject.colour_fg || 'white' : 'white',
          height: '100%',
          borderRadius: '4px',
        }"
      >
        <span
          v-if="calendarType === 'month' && eventParsed.start.hasTime"
          class="mr-1 font-weight-bold ml-1"
        >
          {{ eventParsed.start.time }}
        </span>
        <div
          class="d-flex justify-center align-center flex-grow-1 text-truncate"
        >
          <div class="d-flex justify-center align-center flex-wrap text">
            <lesson-event-link-iterator
              v-if="!selectedEvent.meta.is_member"
              :items="selectedEvent.meta.groups"
              attr="short_name"
              class="mr-1"
            />
            <lesson-event-old-new
              v-if="!selectedEvent.meta.is_teacher || newTeachers.length > 0"
              :new-items="newTeachers"
              :old-items="oldTeachers"
              attr="short_name"
              class="mr-1"
            />

            <lesson-event-subject
              :event="selectedEvent"
              attr="short_name"
              class="font-weight-medium mr-1"
            />
            <lesson-event-old-new
              :new-items="newRooms"
              :old-items="oldRooms"
              attr="short_name"
            />
          </div>
        </div>
      </div>
    </template>
  </base-calendar-feed-event-bar>
</template>

<script>
import calendarFeedEventBarMixin from "aleksis.core/mixins/calendarFeedEventBar.js";
import BaseCalendarFeedEventBar from "aleksis.core/components/calendar/BaseCalendarFeedEventBar.vue";
import lessonEvent from "../mixins/lessonEvent";
import LessonEventSubject from "../../LessonEventSubject.vue";
import LessonEventLinkIterator from "../../LessonEventLinkIterator.vue";
import LessonEventOldNew from "../../LessonEventOldNew.vue";

export default {
  name: "LessonEventBar",
  components: {
    LessonEventOldNew,
    LessonEventLinkIterator,
    LessonEventSubject,
    BaseCalendarFeedEventBar,
  },
  computed: {
    selectedEvent() {
      return this.event;
    },
  },
  mixins: [calendarFeedEventBarMixin, lessonEvent],
};
</script>

<style scoped>
.orange-border {
  border: 3px orange solid;
}

.red-border {
  border: 3px red solid;
}

.text {
  line-height: 1.1;
  font-size: 12px;
}
</style>

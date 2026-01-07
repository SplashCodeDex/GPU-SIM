# Specification: Navigation History (Back/Forward)

## Overview
Implement a navigation history system (Back and Forward) for the NVIDIA Control Panel simulator. This feature will allow users to move between previously visited settings pages using the toolbar buttons, mimicking the behavior of the real application and standard web browsers.

## Functional Requirements
- **History Tracking**: Maintain a stack of visited views (excluding the Home view).
- **Back Navigation**: 
    - Implement a "Back" command that navigates to the previous view in the history stack.
    - Enable the Back button in the toolbar only when there is history to go back to.
    - Tooltip should display the name of the previous view.
- **Forward Navigation**:
    - Implement a "Forward" command that navigates to the next view in the history stack.
    - Enable the Forward button in the toolbar only when there is history to go forward to.
    - Tooltip should display the name of the next view.

## Modern UI/UX Requirements
- **Smooth View Transitions**: Views must cross-fade or slide subtly when changed.
- **NVIDIA Glow Effect**: Navigation buttons should exhibit a soft green glow (`#76B900`) when enabled and hovered.
- **Interactive Breadcrumbs**: The navigation path should use a more dynamic, segments-based layout rather than a single string.
- **Micro-Interactions**: Subtle scale or opacity shifts on button press/hover to provide tactile feedback.
- **Premium Background**: Apply a subtle noise texture to the main content background to add a premium, tactile feel.

## Non-Functional Requirements
- **MVVM Adherence**: History logic should reside in the `MainViewModel` or a dedicated `NavigationService`.
- **UI Consistency**: Use existing `PackIconMaterial` icons in the toolbar.
- **Visual Feedback**: Buttons must be grayed out (disabled) when their respective navigation action is unavailable.

## Acceptance Criteria
- [ ] Users can navigate back to the previous settings page.
- [ ] Users can navigate forward if they have previously gone back.
- [ ] The Back/Forward buttons enable/disable correctly based on history availability.
- [ ] Selecting a new page from the TreeView clears the Forward history.
- [ ] Tooltips correctly identify the destination view.
- [ ] The Home view never appears in the history stack.

## Out of Scope
- Persistence of navigation history across application restarts.
- Mouse button navigation (e.g., Back/Forward buttons on gaming mice).
- Right-click history menu on navigation buttons.

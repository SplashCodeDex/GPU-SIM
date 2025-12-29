# Specification: Navigation History (Back/Forward)

## Overview
Implement a navigation history system (Back and Forward) for the NVIDIA Control Panel simulator. This feature will allow users to move between previously visited settings pages using the toolbar buttons, mimicking the behavior of the real application and standard web browsers.

## Functional Requirements
- **History Tracking**: Maintain a stack of visited views (excluding the Home view).
- **Back Navigation**: 
    - Implement a "Back" command that navigates to the previous view in the history stack.
    - Enable the Back button in the toolbar only when there is history to go back to.
    - Tooltip should display the name of the previous view (e.g., "Back to Manage 3D settings").
- **Forward Navigation**:
    - Implement a "Forward" command that navigates to the next view in the history stack (available after using the Back button).
    - Enable the Forward button in the toolbar only when there is history to go forward to.
    - Tooltip should display the name of the next view.
- **Navigation Interaction**:
    - Navigating to a new page via the TreeView or File menu clears the "Forward" stack and adds the new page to the "Back" stack.
    - Navigating via Back/Forward buttons does not clear the stacks but moves the current position pointer.
- **Home View Exclusion**: The Home view is treated as the root/initial state and is not added to the navigation history stacks.

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

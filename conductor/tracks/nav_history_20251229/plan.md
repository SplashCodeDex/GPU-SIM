# Plan: Navigation History (Back/Forward)

## Phase 1: Foundation & Services [checkpoint: 06a7332]
- [x] Task: Create `INavigationService` and `NavigationService` to manage history stacks. 10f5237
- [x] Task: Write unit tests for `NavigationService` (History tracking, Back/Forward availability, Home exclusion). 10f5237
- [x] Task: Implement `NavigationService` logic. 10f5237
- [x] Task: Conductor - User Manual Verification 'Phase 1: Foundation & Services' (Protocol in workflow.md) 06a7332

## Phase 2: ViewModel Integration [ ]
- [ ] Task: Update `MainViewModel` to inject and use `INavigationService`.
- [ ] Task: Write unit tests for `MainViewModel` navigation commands and button state logic.
- [ ] Task: Implement `BackCommand` and `ForwardCommand` in `MainViewModel`.
- [ ] Task: Update `ExecuteNavigate` to record history via the service (excluding Home).
- [ ] Task: Conductor - User Manual Verification 'Phase 2: ViewModel Integration' (Protocol in workflow.md)

## Phase 3: UI Enhancement [ ]
- [ ] Task: Bind toolbar Back/Forward buttons to `MainViewModel` commands in `MainWindow.xaml`.
- [ ] Task: Update button styles to handle enabled/disabled visual states.
- [ ] Task: Implement dynamic tooltips for navigation buttons based on history names.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: UI Enhancement' (Protocol in workflow.md)

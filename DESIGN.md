# UX/UI Design Document
## ML AutoML Suite

### Design Principles

1. **Simplicity:** Clean, uncluttered interfaces
2. **Clarity:** Clear labels and instructions
3. **Feedback:** Immediate feedback on user actions
4. **Consistency:** Uniform design patterns across pages
5. **Accessibility:** WCAG 2.1 AA compliance

### Color Palette

**Primary Colors:**
- Primary Blue: #0ea5e9 (Primary actions, links)
- Success Green: #10b981 (Success messages)
- Warning Yellow: #f59e0b (Warnings)
- Error Red: #ef4444 (Errors)

**Neutral Colors:**
- Background: #f9fafb (Light gray)
- Surface: #ffffff (White)
- Text Primary: #111827 (Dark gray)
- Text Secondary: #6b7280 (Medium gray)
- Border: #e5e7eb (Light border)

### Typography

- **Headings:** Inter, Bold, 24-32px
- **Body:** Inter, Regular, 16px
- **Labels:** Inter, Medium, 14px
- **Small Text:** Inter, Regular, 12px

### Component Library

#### Buttons
- **Primary:** Blue background, white text, rounded corners
- **Secondary:** Gray background, dark text
- **Danger:** Red background, white text
- **Disabled:** 50% opacity, no interaction

#### Forms
- **Input Fields:** White background, gray border, rounded
- **Labels:** Above inputs, medium weight
- **Validation:** Red border and message on error
- **Success:** Green border on valid input

#### Cards
- **Container:** White background, shadow, rounded corners
- **Padding:** 24px
- **Spacing:** 16px between elements

### Page Layouts

#### Streamlit Interface

**Layout:**
- Sidebar: Navigation, API URL input
- Main Area: Content based on selected page
- Width: Wide layout for data tables

**Navigation:**
- Vertical sidebar menu
- Icons + text labels
- Active state highlighting

#### Next.js Interface

**Layout:**
- Header: Title and description
- Tab Navigation: Horizontal tabs
- Content Area: White card with content
- Footer: (Optional) Version info

**Responsive Breakpoints:**
- Mobile: < 768px (Stacked layout)
- Tablet: 768px - 1024px (2 columns)
- Desktop: > 1024px (Full width)

### User Flows

#### Flow 1: Complete ML Pipeline

1. **Data Upload Page**
   - User selects upload method
   - Uploads file or connects to DB
   - System shows data preview
   - User proceeds to training

2. **Model Training Page**
   - System shows column list
   - User selects X and Y columns
   - Clicks "Train Models"
   - System shows progress
   - Results displayed in table

3. **Model Comparison Page**
   - User selects models to compare
   - System shows comparison chart
   - User reviews metrics

4. **Predictions Page**
   - User uploads new data
   - System makes predictions
   - Results displayed and downloadable

#### Flow 2: Quick Prediction

1. User goes to Predictions page
2. Selects saved model
3. Uploads data file
4. Gets predictions immediately

### Component Specifications

#### DataUpload Component
- **File Upload:**
  - Drag-and-drop zone
  - File type indicators
  - Progress bar
  - Success/error messages

- **Database Connection:**
  - Connection string input (password type)
  - Database/table selection
  - Test connection button
  - Connection status indicator

#### ModelTraining Component
- **Column Selection:**
  - Multi-select for X columns
  - Single select for Y column
  - Column info (type, missing values)
  - Validation messages

- **Training Progress:**
  - Progress bar
  - Current model being trained
  - Estimated time remaining

- **Results Display:**
  - Metrics table
  - Best model highlight
  - Download results option

#### Predictions Component
- **Input:**
  - File upload
  - Manual entry form (dynamic based on features)
  - Data preview

- **Output:**
  - Predictions table
  - Download CSV button
  - Statistics summary

#### ModelComparison Component
- **Model Selection:**
  - Checkbox list
  - Select all/none
  - Model metadata display

- **Comparison Chart:**
  - Bar chart for metrics
  - Interactive tooltips
  - Export chart option

#### Reports Component
- **Model Selection:**
  - Dropdown with model list
  - Model metadata

- **Report Sections:**
  - Metrics overview (cards)
  - Detailed metrics table
  - Visualization charts
  - Model parameters

### Accessibility Features

- **Keyboard Navigation:** All interactive elements accessible via keyboard
- **Screen Readers:** ARIA labels on all components
- **Color Contrast:** Minimum 4.5:1 for text
- **Focus Indicators:** Clear focus states on all inputs
- **Error Messages:** Descriptive, actionable error messages

### Responsive Design

#### Mobile (< 768px)
- Stacked layout
- Full-width buttons
- Collapsible sections
- Bottom navigation (optional)

#### Tablet (768px - 1024px)
- 2-column grid where appropriate
- Side-by-side forms
- Maintained spacing

#### Desktop (> 1024px)
- Full layout
- Optimal spacing
- Hover states
- Multi-column tables

### Animation and Transitions

- **Page Transitions:** Fade in (300ms)
- **Button Hover:** Scale 1.02 (150ms)
- **Loading States:** Spinner animation
- **Success Messages:** Slide in from top (300ms)

### Error States

- **Validation Errors:** Red border, message below input
- **API Errors:** Toast notification, error message
- **Network Errors:** Retry button, offline indicator
- **Empty States:** Helpful message, action button

### Loading States

- **Skeleton Screens:** For data loading
- **Progress Bars:** For long operations
- **Spinners:** For quick operations
- **Percentage:** For file uploads

### Success States

- **Success Messages:** Green banner, auto-dismiss
- **Confirmation Dialogs:** For destructive actions
- **Success Icons:** Checkmark animations

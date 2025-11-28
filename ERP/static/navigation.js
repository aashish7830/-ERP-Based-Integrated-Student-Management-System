// Dynamic Navigation Configuration
const NAVIGATION_CONFIG = {
  // Main navigation items for student portal pages (in logical sequence)
  mainNav: [
    {
      id: 'dashboard',
      title: 'PROFILE',
      href: '/dashboard/',
      icon: 'bi-person-circle',
      active: false,
      order: 1,
      description: 'Student profile and personal information'
    },
    {
      id: 'attendance',
      title: 'ATTENDANCE',
      href: '/attendance/',
      icon: 'bi-calendar-check',
      active: false,
      order: 2,
      description: 'View attendance records and reports'
    },
    {
      id: 'fees',
      title: 'FEE DETAILS',
      href: '/fees/',
      icon: 'bi-credit-card',
      active: false,
      order: 3,
      description: 'Fee structure, payments and receipts'
    },
    {
      id: 'transport-fee',
      title: 'TRANSPORT FEE',
      href: '/transport-fee/',
      icon: 'bi-bus-front',
      active: false,
      order: 4,
      description: 'Transport fee application and payment'
    },
    {
      id: 'examination',
      title: 'EXAMINATION',
      href: '/examination/',
      icon: 'bi-journal-text',
      active: false,
      order: 5,
      description: 'Exam schedules, forms and results'
    },
    {
      id: 'result',
      title: 'RESULT',
      href: '/result/',
      icon: 'bi-trophy',
      active: false,
      order: 6,
      description: 'View exam results and grades'
    },
    {
      id: 'library',
      title: 'LIBRARY',
      href: '/library/',
      icon: 'bi-book',
      active: false,
      order: 7,
      description: 'Library books and resources'
    },
    {
      id: 'registration',
      title: 'REGISTRATION',
      href: '/registration/',
      icon: 'bi-pencil-square',
      active: false,
      order: 8,
      description: 'Semester and course registration'
    },
    {
      id: 'assignment',
      title: 'ASSIGNMENTS',
      href: '/assignment/',
      icon: 'bi-clipboard-check',
      active: false,
      order: 9,
      description: 'Assignment submission and tracking'
    },
    {
      id: 'class',
      title: 'CLASSES',
      href: '/class/',
      icon: 'bi-calendar-week',
      active: false,
      order: 10,
      description: 'Class schedule and attendance tracking'
    },
    {
      id: 'events',
      title: 'EVENTS',
      href: '/events/',
      icon: 'bi-calendar-event',
      active: false,
      order: 11,
      description: 'College events and activities management'
    },
    {
      id: 'calendar',
      title: 'CALENDAR',
      href: '/calendar/',
      icon: 'bi-calendar3',
      active: false,
      order: 12,
      description: 'College academic calendar and important dates'
    },
    {
      id: 'placement',
      title: 'PLACEMENT',
      href: '/placement/',
      icon: 'bi-briefcase',
      active: false,
      order: 13,
      description: 'Job opportunities and placement information'
    },
    {
      id: 'application-center',
      title: 'APPLICATION CENTER',
      href: '/application-center/',
      icon: 'bi-file-earmark-text',
      active: false,
      order: 14,
      description: 'Submit applications for certificates, leave, and other requests'
    }
  ],
  
  // Public navigation for landing page
  publicNav: [
    {
      id: 'college-info',
      title: 'College Info',
      href: '/college-info/',
      icon: 'bi-building',
      order: 1,
      description: 'About college, courses and facilities'
    },
    {
      id: 'admissions',
      title: 'Admissions',
      href: '#admissions',
      icon: 'bi-mortarboard',
      order: 2,
      description: 'Admission process and requirements'
    },
    {
      id: 'finance',
      title: 'Fees',
      href: '#finance',
      icon: 'bi-currency-dollar',
      order: 3,
      description: 'Fee structure and payment options'
    },
    {
      id: 'hostel',
      title: 'Hostel',
      href: '#hostel',
      icon: 'bi-house',
      order: 4,
      description: 'Hostel facilities and accommodation'
    },
    {
      id: 'analytics',
      title: 'Dashboard',
      href: '#analytics',
      icon: 'bi-graph-up',
      order: 5,
      description: 'College statistics and achievements'
    }
  ],

  // Admin navigation (separate from student portal)
  adminNav: [
    {
      id: 'admin-registration',
      title: 'Student Registration',
      href: '/admin-student-registration/',
      icon: 'bi-person-plus',
      order: 1,
      description: 'Register new students'
    }
  ]
  ,
  // Faculty navigation (separate from student portal)
  facultyNav: [
    { id: 'faculty-profile', title: 'PROFILE', href: '/faculty-portal/', icon: 'bi-person-badge', order: 1, description: 'Faculty profile and personal information' },
    { id: 'faculty-attendance', title: 'ATTENDANCE', href: '/attendance/', icon: 'bi-calendar-check', order: 2, description: 'Mark and view attendance' },
    { id: 'faculty-program', title: 'PROGRAM', href: '/faculty-portal/', icon: 'bi-journal-bookmark', order: 3, description: 'Program/curriculum details' },
    { id: 'faculty-mentorship', title: 'MENTORSHIP DETAILS', href: '/faculty-portal/', icon: 'bi-people', order: 4, description: 'Mentorship assignments and notes' },
    { id: 'faculty-examination', title: 'EXAMINATION', href: '/examination/', icon: 'bi-clipboard-data', order: 5, description: 'Exam duties, question papers, evaluations' },
    { id: 'faculty-hr', title: 'HR', href: '/hr-department/', icon: 'bi-person-gear', order: 6, description: 'Leave, payroll and HR services' },
    { id: 'faculty-library', title: 'LIBRARY', href: '/library/', icon: 'bi-book', order: 7, description: 'Library services for faculty' },
    { id: 'faculty-others', title: 'OTHERS', href: '/faculty-portal/', icon: 'bi-grid', order: 8, description: 'Miscellaneous tools' },
    { id: 'faculty-mentor-mentee', title: 'MENTOR-MENTEE', href: '/faculty-portal/', icon: 'bi-person-hearts', order: 9, description: 'Mentor-mentee interactions' }
  ]
};

// Navigation utility functions
class NavigationManager {
  constructor() {
    this.currentPage = this.getCurrentPageId();
    this.setActivePage();
  }

  getCurrentPageId() {
    // Map URL paths to page IDs (Django URLs)
    const path = window.location.pathname;
    const pathMap = {
      '/': 'home',
      '/dashboard/': 'dashboard',
      '/attendance/': 'attendance',
      '/fees/': 'fees',
      '/transport-fee/': 'transport-fee',
      '/examination/': 'examination',
      '/result/': 'result',
      '/library/': 'library',
      '/registration/': 'registration',
      '/assignment/': 'assignment',
      '/class/': 'class',
      '/events/': 'events',
      '/calendar/': 'calendar',
      '/placement/': 'placement',
      '/application-center/': 'application-center',
      '/application-center/': 'application-center',
      '/syllabus/': 'syllabus',
      '/hostel/': 'hostel',
      '/college-info/': 'college-info',
      '/admin-student-registration/': 'admin-registration',
      '/admin-dashboard/': 'admin-dashboard',
      '/faculty-portal/': 'faculty-portal',
      '/internal-datesheet/': 'examination',
      '/external-datesheet/': 'examination',
      '/exam-form-main/': 'examination',
      '/exam-form-reappear/': 'examination',
    };
    
    return pathMap[path] || 'home';
  }

  setActivePage() {
    // Reset all active states first
    NAVIGATION_CONFIG.mainNav.forEach(nav => {
      nav.active = false;
    });
    
    // Set active state for current page
    NAVIGATION_CONFIG.mainNav.forEach(nav => {
      if (nav.id === this.currentPage) {
        nav.active = true;
      }
    });
    
    // Also check admin navigation
    if (NAVIGATION_CONFIG.adminNav) {
      NAVIGATION_CONFIG.adminNav.forEach(nav => {
        nav.active = nav.id === this.currentPage;
      });
    }
  }

  renderMainNavigation(containerId = 'moduleTabs') {
    const container = document.getElementById(containerId);
    if (!container) return;

    // Sort navigation items by order
    const sortedNav = [...NAVIGATION_CONFIG.mainNav].sort((a, b) => (a.order || 0) - (b.order || 0));

    const navHTML = sortedNav.map(nav => {
      const isActive = nav.active;
      const buttonClass = isActive 
        ? 'btn btn-warning text-white' 
        : 'btn btn-outline-warning';
      
      // Ensure href is absolute path (starts with /)
      let href = nav.href || '';
      // Force absolute path - remove any .html extension and ensure leading slash
      if (href) {
        // Remove .html if present
        href = href.replace(/\.html$/, '');
        // Remove any leading dots or slashes that might make it relative
        href = href.replace(/^\.\.?\//, '');
        // Ensure it starts with /
        if (!href.startsWith('/') && !href.startsWith('http') && !href.startsWith('#')) {
          href = '/' + href;
        }
        // Ensure it ends with / for Django URLs
        if (href.startsWith('/') && !href.endsWith('/') && !href.includes('?')) {
          href = href + '/';
        }
      }
      
      return `
        <li class="nav-item">
          ${isActive 
            ? `<span class="${buttonClass}" title="${nav.description || ''}">${nav.title}</span>`
            : `<a class="${buttonClass}" href="${href}" title="${nav.description || ''}">
                 <i class="${nav.icon} me-1"></i>${nav.title}
               </a>`
          }
        </li>
      `;
    }).join('');

    container.innerHTML = navHTML;
  }

  renderPublicNavigation(containerId = 'navMenu') {
    const container = document.getElementById(containerId);
    if (!container) return;

    // Sort public navigation by order
    const sortedNav = [...NAVIGATION_CONFIG.publicNav].sort((a, b) => (a.order || 0) - (b.order || 0));

    const navHTML = sortedNav.map(nav => {
      // Ensure href is absolute path (starts with /)
      let href = nav.href || '';
      if (href && !href.startsWith('/') && !href.startsWith('http') && !href.startsWith('#')) {
        href = '/' + href;
      }
      return `
      <li class="nav-item">
        <a class="nav-link" href="${href}" title="${nav.description || ''}">
          <i class="${nav.icon} me-1"></i>${nav.title}
        </a>
      </li>
    `;
    }).join('');

    container.innerHTML = navHTML;
  }

  renderAdminNavigation(containerId = 'adminTabs') {
    const container = document.getElementById(containerId);
    if (!container) return;

    // Sort admin navigation by order
    const sortedNav = [...(NAVIGATION_CONFIG.adminNav || [])].sort((a, b) => (a.order || 0) - (b.order || 0));

    const navHTML = sortedNav.map(nav => {
      const isActive = nav.active;
      const buttonClass = isActive 
        ? 'btn btn-danger text-white' 
        : 'btn btn-outline-danger';
      
      // Ensure href is absolute path (starts with /)
      let href = nav.href || '';
      if (href && !href.startsWith('/') && !href.startsWith('http') && !href.startsWith('#')) {
        href = '/' + href;
      }
      
      return `
        <li class="nav-item">
          ${isActive 
            ? `<span class="${buttonClass}" title="${nav.description || ''}">${nav.title}</span>`
            : `<a class="${buttonClass}" href="${href}" title="${nav.description || ''}">
                 <i class="${nav.icon} me-1"></i>${nav.title}
               </a>`
          }
        </li>
      `;
    }).join('');

    container.innerHTML = navHTML;
  }

  renderFacultyNavigation(containerId = 'facultyTabs') {
    const container = document.getElementById(containerId);
    if (!container) return;

    // Determine current faculty page active state
    const current = this.currentPage;
    const sortedNav = [...(NAVIGATION_CONFIG.facultyNav || [])].sort((a, b) => (a.order || 0) - (b.order || 0));

    const navHTML = sortedNav.map(nav => {
      const isActive = nav.id === current;
      const buttonClass = isActive ? 'btn btn-warning text-white' : 'btn btn-outline-warning';
      
      // Ensure href is absolute path (starts with /)
      let href = nav.href || '';
      if (href && !href.startsWith('/') && !href.startsWith('http') && !href.startsWith('#')) {
        href = '/' + href;
      }
      
      return `
        <li class="nav-item">
          ${isActive
            ? `<span class="${buttonClass}" title="${nav.description || ''}">${nav.title}</span>`
            : `<a class="${buttonClass}" href="${href}" title="${nav.description || ''}">
                 <i class="${nav.icon} me-1"></i>${nav.title}
               </a>`
          }
        </li>
      `;
    }).join('');

    container.innerHTML = navHTML;
  }

  // Add new navigation item dynamically
  addNavigationItem(item, isMainNav = true) {
    if (isMainNav) {
      NAVIGATION_CONFIG.mainNav.push(item);
    } else {
      NAVIGATION_CONFIG.publicNav.push(item);
    }
  }

  // Remove navigation item
  removeNavigationItem(id, isMainNav = true) {
    if (isMainNav) {
      NAVIGATION_CONFIG.mainNav = NAVIGATION_CONFIG.mainNav.filter(nav => nav.id !== id);
    } else {
      NAVIGATION_CONFIG.publicNav = NAVIGATION_CONFIG.publicNav.filter(nav => nav.id !== id);
    }
  }

  // Update navigation item
  updateNavigationItem(id, updates, isMainNav = true) {
    const navArray = isMainNav ? NAVIGATION_CONFIG.mainNav : NAVIGATION_CONFIG.publicNav;
    const index = navArray.findIndex(nav => nav.id === id);
    
    if (index !== -1) {
      navArray[index] = { ...navArray[index], ...updates };
    }
  }

  // Get navigation item by ID
  getNavigationItem(id, isMainNav = true) {
    const navArray = isMainNav ? NAVIGATION_CONFIG.mainNav : NAVIGATION_CONFIG.publicNav;
    return navArray.find(nav => nav.id === id);
  }

  // Get all navigation items
  getAllNavigationItems(isMainNav = true) {
    return isMainNav ? NAVIGATION_CONFIG.mainNav : NAVIGATION_CONFIG.publicNav;
  }
}

// Initialize navigation when DOM is loaded
function initNavigation() {
  // Create new NavigationManager instance (will detect current page)
  window.navigationManager = new NavigationManager();
  
  // Auto-render navigation if containers exist
  if (document.getElementById('moduleTabs')) {
    window.navigationManager.renderMainNavigation();
  }
  
  if (document.getElementById('navMenu')) {
    window.navigationManager.renderPublicNavigation();
  }
  
  if (document.getElementById('adminTabs')) {
    window.navigationManager.renderAdminNavigation();
  }

  if (document.getElementById('facultyTabs')) {
    window.navigationManager.renderFacultyNavigation();
  }
}

// Handle both cases: DOM already loaded or still loading
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initNavigation);
} else {
  // DOM already loaded, initialize immediately
  // Use setTimeout to ensure all scripts are loaded
  setTimeout(initNavigation, 0);
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { NavigationManager, NAVIGATION_CONFIG };
}

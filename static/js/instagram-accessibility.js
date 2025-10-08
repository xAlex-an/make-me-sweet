/**
 * Instagram Embed Accessibility Enhancement
 * Automatically adds proper title and aria-label attributes to Instagram iframes
 * for better accessibility compliance with Lighthouse audits
 */

// Instagram iframe titles mapping
const INSTAGRAM_TITLES = [
  'Instagram Reel 1 - Baking Recipe Tutorial',
  'Instagram Reel 2 - Sweet Dessert Making',
  'Instagram Reel 3 - Cake Decoration Techniques'
];

/**
 * Processes an Instagram iframe to add accessibility attributes
 * @param {HTMLIFrameElement} iframe - The iframe element to process
 */
function processInstagramIframe(iframe) {
  if (!iframe.title || iframe.title.trim() === '') {
    // Find the parent blockquote to get the index
    const parent = iframe.closest('.instagram-media');
    if (parent) {
      let index = 0;
      if (parent.classList.contains('instagram-embed-1')) {index = 1;}
      else if (parent.classList.contains('instagram-embed-2')) {index = 2;}
      
      const title = INSTAGRAM_TITLES[index] || 'Instagram embed content';
      iframe.title = title;
      iframe.setAttribute('aria-label', title);
      
      console.log(`Added title "${title}" to Instagram iframe`);
    }
  }
}

/**
 * Main function to add accessibility attributes to Instagram iframes
 */
function addInstagramAccessibility() {
  // Create a mutation observer to watch for dynamically added Instagram iframes
  const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      mutation.addedNodes.forEach(function(node) {
        if (node.nodeType === 1) { // Element node
          // Check if the added node is an Instagram iframe
          if (node.tagName === 'IFRAME' && node.src && node.src.includes('instagram.com')) {
            processInstagramIframe(node);
          }
          
          // Find all Instagram iframes within the added node
          if (node.querySelectorAll) {
            const iframes = node.querySelectorAll('iframe[src*="instagram.com"]');
            iframes.forEach(processInstagramIframe);
          }
        }
      });
    });
  });
  
  // Start observing the document for changes
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
  
  // Check for existing iframes that might already be loaded
  const checkExistingIframes = () => {
    const existingIframes = document.querySelectorAll('iframe[src*="instagram.com"]');
    existingIframes.forEach(processInstagramIframe);
  };
  
  // Check immediately
  checkExistingIframes();
  
  // Check after 1 second (for faster connections)
  setTimeout(checkExistingIframes, 1000);
  
  // Check after 3 seconds (for slower connections)
  setTimeout(checkExistingIframes, 3000);
  
  // Check after 5 seconds (final fallback)
  setTimeout(checkExistingIframes, 5000);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', addInstagramAccessibility);
} else {
  addInstagramAccessibility();
}

// Export for potential use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { addInstagramAccessibility, processInstagramIframe };
}
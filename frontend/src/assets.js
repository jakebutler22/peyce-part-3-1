export const decorativeObjects = {
  'satin-bow': { id: 'satin-bow', slot: 'opening', source: '/assets/bow.png', material: 'satin', colorVariants: ['ballet-pink'], desktopPlacement: 'upper-left of opening composition', mobilePlacement: 'above opening title', width: 360, aspectRatio: 1024 / 670, decorative: true, reducedMotion: 'static at all times', provenance: 'Original built-in image generation; see docs/assets/provenance.md' },
  'satin-bow-small': { id: 'satin-bow-small', slot: 'checkin', source: '/assets/bow.png', material: 'satin', colorVariants: ['ballet-pink'], desktopPlacement: 'quiet check-in header', mobilePlacement: 'hidden during check-in', width: 72, aspectRatio: 1024 / 670, decorative: true, reducedMotion: 'static at all times', provenance: 'Second registered presentation instance of original satin bow' },
};
export const pacingObject = { id: 'latex-balloon', source: '/assets/balloon.png', material: 'latex', colors: ['pink', 'red', 'pearl'], normalizedInput: 'inflation in [0,1]', decorative: false, reducedMotion: 'fixed size with phase text and small progress bar', provenance: 'Original generated image, deformation experiment; see docs/assets/provenance.md' };

export const objectsFor = slot => Object.values(decorativeObjects).filter(object => object.slot === slot);

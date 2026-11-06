// No third-party frames or thumbnail requests until the reader chooses a video.
for(const card of document.querySelectorAll('[data-youtube-id]')) {
  const button=card.querySelector('[data-load-video]');
  const close=card.querySelector('[data-close-video]');
  const slot=card.querySelector('.embed-slot');
  const status=card.querySelector('.embed-status');
  const id=card.dataset.youtubeId;
  if(!/^[A-Za-z0-9_-]{11}$/.test(id))continue;
  button.hidden=false;
  button.addEventListener('click',()=>{
    const frame=document.createElement('iframe');
    frame.src=`https://www.youtube-nocookie.com/embed/${id}?autoplay=0&rel=0`;
    frame.title=card.dataset.videoTitle;
    frame.referrerPolicy='strict-origin-when-cross-origin';
    frame.allow='encrypted-media; picture-in-picture; fullscreen';
    frame.allowFullscreen=true;
    slot.replaceChildren(frame);slot.hidden=false;button.hidden=true;close.hidden=false;
    status.textContent='YouTube player requested. If playback is unavailable here, use the original video link below.';
    frame.focus();
  });
  close.addEventListener('click',()=>{slot.replaceChildren();slot.hidden=true;close.hidden=true;button.hidden=false;status.textContent='';button.focus();});
}
// Native playback controls provide pause, seek, captions and fullscreen. Avoid
// competing sound/motion if the reader starts another local teaching clip.
const localVideos=[...document.querySelectorAll('video.local-motion')];
for(const video of localVideos)video.addEventListener('play',()=>{
  for(const other of localVideos)if(other!==video)other.pause();
});
window.addEventListener('beforeprint',()=>{for(const video of localVideos)video.pause();});

// Figures keep ordinary image links when JavaScript is unavailable.
const figureLinks=[...document.querySelectorAll('.figure-link')];
const gallery=document.querySelector('#figure-gallery');
if(gallery&&typeof gallery.showModal==='function'){
  const picture=gallery.querySelector('img'),count=gallery.querySelector('[data-figure-count]'),caption=gallery.querySelector('[data-figure-caption]');
  const zoom=gallery.querySelector('[data-figure-zoom]');let index=0,origin=null;
  const show=i=>{
    index=(i+figureLinks.length)%figureLinks.length;
    const link=figureLinks[index],original=link.querySelector('img');
    picture.src=link.href;picture.alt=original.alt;caption.textContent=original.alt;count.textContent=`Figure ${index+1} of ${figureLinks.length}`;
    gallery.classList.remove('zoomed');zoom.setAttribute('aria-pressed','false');zoom.textContent='Zoom in';
    gallery.querySelector('[data-figure-original]').href=link.href;
  };
  figureLinks.forEach((link,i)=>link.addEventListener('click',event=>{
    if(event.ctrlKey||event.metaKey||event.shiftKey||event.altKey||event.button!==0)return;
    event.preventDefault();origin=link;show(i);gallery.showModal();
  }));
  gallery.querySelector('[data-figure-prev]').addEventListener('click',()=>show(index-1));
  gallery.querySelector('[data-figure-next]').addEventListener('click',()=>show(index+1));
  gallery.querySelector('[data-figure-close]').addEventListener('click',()=>gallery.close());
  gallery.addEventListener('close',()=>{if(origin)origin.focus({preventScroll:true});});
  gallery.addEventListener('keydown',event=>{
    if(event.key==='ArrowLeft'){event.preventDefault();show(index-1);}
    if(event.key==='ArrowRight'){event.preventDefault();show(index+1);}
  });
  zoom.addEventListener('click',()=>{const enlarged=gallery.classList.toggle('zoomed');zoom.setAttribute('aria-pressed',String(enlarged));zoom.textContent=enlarged?'Fit to view':'Zoom in';});
}

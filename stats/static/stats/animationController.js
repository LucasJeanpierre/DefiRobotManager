/**
 * Author : Lucas JEANPIERRE
 * 
 * AnimationController object
 * 
 */


const AnimationController = {
    animationInterval: Array(),
    animationTimeOut: Array(Array()),
    isAnimationLooping: Array(),
    isAnimationRunning: Array(),

    /**
     * AnimationController.startAnimation
     * 
     * @param string elementId
     * @param int count default : 0
     * 
     * start the animation of the wanted element
     * 
     * no count attribute given -> infinite loop
     * 
     * example : AnimationController.startAnimation('myElementId', 3)
     * 
     */
    startAnimation: function(elementId, count = 0) {
        element = document.getElementById(elementId);
        if (element != null) {
            var animationClass = element.getAttribute('data-animationClass');
            if (animationClass != null) {
                element.classList.add(animationClass)
                if (element.style.animationPlayState == 'paused') element.style.animationPlayState = 'running';
                if (parseInt(count) > 0) {
                    setTimeout(() => {
                        AnimationController.pauseAnimation(elementId)
                    }, parseFloat(getComputedStyle(element).animationDuration) * 1000 * parseInt(count))
                }
            } else {
                console.warn('AnimationController : The element do not have data-animationClass attribute');
            }
        } else {
            console.warn('AnimationController : No element found');
        }
    },

    /**
     * AnimationController.stopAnimation
     * 
     * @param string elementId
     * 
     * stop the animation of the wanted element and set the element at its orginial state
     * 
     * example : AnimationController.stopAnimation('myElementId')
     */
    stopAnimation: function(elementId) {
        element = document.getElementById(elementId);
        if (element != null) {
            var animationClass = element.getAttribute('data-animationClass');
            if (animationClass != null) {
                if (element.style.animationPlayState == 'running') element.style.animationPlayState = 'paused';
                element.classList.remove(animationClass)
            } else {
                console.warn('AnimationController : The element do not have data-animationClass attribute');
            }
        } else {
            console.warn('AnimationController : No element found');
        }
    },

    /**
     * AnimationController.pauseAnimation
     * 
     * @param string elementId
     * 
     * pause the animation at its current state
     * 
     * example : AnimationController.pauseAnimation('myElementId')
     */
    pauseAnimation: function(elementId) {
        element = document.getElementById(elementId);
        if (element != null) {
            var animationClass = element.getAttribute('data-animationClass');
            if (animationClass != null) {
                element.style.animationPlayState = 'paused';
            } else {
                console.warn('AnimationController : The element do not have data-animationClass attribute');
            }
        } else {
            console.warn('AnimationController : No element found');
        }
    },

    /**
     * AnimationController.startAnimationByElement
     * 
     * @param DOM element
     * @param int count default : 0
     * 
     * start the animation of the given element
     * 
     * no count attribute given -> infinite loop
     * 
     * example : AnimationController.startAnimation(myElement, 3)
     * 
     */
    startAnimationByElement: function(element, count = 0) {
        if (element != null) {
            var animationClass = element.getAttribute('data-animationClass');
            if (animationClass != null) {
                element.classList.add(animationClass)
                if (element.style.animationPlayState == 'paused') element.style.animationPlayState = 'running';
                if (parseInt(count) > 0) {
                    setTimeout(() => {
                        AnimationController.pauseAnimationByElement(element)
                    }, parseFloat(getComputedStyle(element).animationDuration) * 1000 * parseInt(count))
                }
            } else {
                console.warn('AnimationController : The element do not have data-animationClass attribute');
            }
        } else {
            console.warn('AnimationController : No element found');
        }
    },

    /**
     * AnimationController.stopAnimationByElement
     * 
     * @param DOM element
     * 
     * stop the animation of the given element and set the element at its orginial state
     * 
     * example : AnimationController.stopAnimation(myElement)
     */
    stopAnimationByElement: function(element) {
        if (element != null) {
            var animationClass = element.getAttribute('data-animationClass');
            if (animationClass != null) {
                if (element.style.animationPlayState == 'running') element.style.animationPlayState = 'paused';
                element.classList.remove(animationClass)
            } else {
                console.warn('AnimationController : The element do not have data-animationClass attribute');
            }
        } else {
            console.warn('AnimationController : No element found');
        }
    },

    /**
     * AnimationController.pauseAnimationByElement
     * 
     * @param DOM element
     * 
     * pause the animation at its current state
     * 
     * example : AnimationController.pauseAnimation(myElement)
     */
    pauseAnimationByElement: function(element) {
        if (element != null) {
            var animationClass = element.getAttribute('data-animationClass');
            if (animationClass != null) {
                element.style.animationPlayState = 'paused';
            } else {
                console.warn('AnimationController : The element do not have data-animationClass attribute');
            }
        } else {
            console.warn('AnimationController : No element found');
        }
    },

    /**
     * AnimationController.startElementOfGlobalAnimation
     * 
     * @param DOM element
     * 
     * Start the animation af an element of the globalAnimation
     * 
     * example : AnimationController.startElementOfGlobalAnimation(myElement)
     */
    startElementOfGlobalAnimation: function(element) {
        var animationClass = element.getAttribute('data-animationClass');
        if (animationClass != null) {
            if (element.style.animationPlayState == 'paused') element.style.animationPlayState = 'running';
            if (!element.classList.contains(animationClass)) {
                element.classList.add(animationClass)
                setTimeout(() => {
                    element.classList.remove(animationClass)
                }, parseFloat(getComputedStyle(element).animationDuration) * 1000);
            } else {
                element.classList.toggle(animationClass)
            }
        } else {
            console.warn('AnimationController : The element do not have data-animationClass attribute');
        }
    },

    /**
     * AnimationController.stopElementOfGlobalAnimation
     * 
     * @param DOM element
     * 
     * Stop the animation af an element of the globalAnimation
     * 
     * example : AnimationController.stopElementOfGlobalAnimation(myElement)
     */
    stopElementOfGlobalAnimation: function(element) {
        var animationClass = element.getAttribute('data-animationClass');
        if (animationClass != null) {
            if (element.style.animationPlayState == 'running') element.style.animationPlayState = 'paused';
            if (element.classList.contains(animationClass)) {
                element.classList.remove(animationClass)
            }
        } else {
            console.warn('AnimationController : The element do not have data-animationClass attribute');
        }
    },

    /**
     * AnimationController.startGlobalAnimation
     * 
     * @param string globalAnimationName
     * @param float elementDelay
     * 
     * start the wanted global animation
     * 
     * elementDelay -> delay between each animated object in seconds
     * 
     * example : AnimationController.startGlobalAnimation('myGlobalAnimationName', 1.5)
     * 
     * 
     */
    startGlobalAnimation: function(globalAnimationName, elementDelay) {
        if ((this.isAnimationRunning[globalAnimationName] == false) || (this.isAnimationRunning[globalAnimationName] == undefined)) {
            this.isAnimationRunning[globalAnimationName] = true;
            this.animationTimeOut[globalAnimationName] = Array();
            document.querySelectorAll('[data-globalAnimationName="' + globalAnimationName + '"]').forEach(element => {
                if (this.animationTimeOut[globalAnimationName][element.getAttribute('data-globalAnimationOrder')] != null) clearTimeout(this.animationTimeOut[globalAnimationName][element.getAttribute('data-globalAnimationOrder')]);
                this.animationTimeOut[globalAnimationName][element.getAttribute('data-globalAnimationOrder')] = setTimeout(() => {
                    this.startElementOfGlobalAnimation(element);
                    this.isAnimationRunning[globalAnimationName] = false;
                }, parseInt(element.getAttribute('data-globalAnimationOrder')) * elementDelay * 1000);

            })
        } else {
            console.warn('AnimationController : The animation is aleady running');
        }
    },

    /**
     * AnimationController.startGlobalAnimationLoop
     * 
     * @param string globalAnimationName
     * @param float elementDelay
     * @param float loopDuration
     * 
     * loop the wanted global animation 
     * 
     * elementDelay -> delay between each animated object in seconds
     * 
     * loopDuration -> delay between each start of the globalAnimation
     * 
     * example : AnimationController.startGlobalAnimationLoop('myGlobalAnimationName', 1.5)
     * 
     * !! loopDuration must be smaller than the animationDuration
     */
    startGlobalAnimationLoop: function(globalAnimationName, elementDelay, loopDuration) {
        if (!this.isAnimationLooping[globalAnimationName]) {
            if (loopDuration > elementDelay) {
                this.startGlobalAnimation(globalAnimationName, elementDelay)
                this.isAnimationLooping[globalAnimationName] = true;
                AnimationController.animationInterval[globalAnimationName] = setInterval(() => {
                    this.startGlobalAnimation(globalAnimationName, elementDelay)
                }, loopDuration * 1000);
            } else {
                console.warn('AnimationController : The loopDuration cannot be higher than element delay');
            }
        } else {
            console.warn('AnimationController : The animation is already looping');
        }
    },

    /**
     * AnimationController.stopGlobalAnimationLoop
     * 
     * @param string globalAnimationName
     * 
     * stop the wanted globalAnimation imediately
     * 
     * example : AnimationController.stopGlobalAnimationLoop('myGlobalAnimationName')
     * 
     */
    stopGlobalAnimationLoop: function(globalAnimationName) {
        document.querySelectorAll('[data-globalAnimationName="' + globalAnimationName + '"]').forEach(element => {
            this.stopElementOfGlobalAnimation(element);
            clearTimeout(this.animationTimeOut[globalAnimationName][element.getAttribute('data-globalAnimationOrder')])
        })
        clearInterval(AnimationController.animationInterval[globalAnimationName]);
        this.isAnimationLooping[globalAnimationName] = false;
    },

    /**
     * AnimationController.endGlobalAnimationLoop
     * 
     * @param string globalAnimationName
     * 
     * stop the looping of the wanted globalAnimation
     * 
     * example : AnimationController.endGlobalAnimationLoop('myGlobalAnimationName')
     * 
     */
    endGlobalAnimationLoop: function(globalAnimationName) {
        clearInterval(AnimationController.animationInterval[globalAnimationName]);
        this.isAnimationLooping[globalAnimationName] = false;
    },


    /**
     * AnimationController.init
     * 
     * @param none
     * 
     * attach start/stop/pause function to dom element with the data-animationClass attribute
     */
    init: function() {
        document.querySelectorAll("[data-animationClass]").forEach(element => {
            element.startAnimation = function(count = 0) { AnimationController.startAnimationByElement(element, count) };
            element.stopAnimation = function() { AnimationController.stopAnimationByElement(element) };
            element.pauseAnimation = function() { AnimationController.pauseAnimationByElement(element) };
        })
    }

}
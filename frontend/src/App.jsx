import React, { useState } from 'react'
import './App.css'

function App() {
  const [showBookingModal, setShowBookingModal] = useState(false)
  const [selectedService, setSelectedService] = useState('')
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    date: '',
    startTime: '',
    endTime: '',
    notes: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitMessage, setSubmitMessage] = useState('')

  const services = [
    {
      id: 'studio-access',
      title: 'Studio Access',
      description: 'Full access to our professional recording studio',
      price: '$150/hour'
    },
    {
      id: 'engineer-request',
      title: 'Engineer Request',
      description: 'Professional engineer assistance for your recording',
      price: '$200/hour'
    },
    {
      id: 'mixing',
      title: 'Mixing',
      description: 'Professional mixing services for your tracks',
      price: '$300/song'
    }
  ]

  const openBookingModal = (serviceId) => {
    setSelectedService(serviceId)
    setShowBookingModal(true)
    setSubmitMessage('')
  }

  const closeBookingModal = () => {
    setShowBookingModal(false)
    setSelectedService('')
    setFormData({
      name: '',
      email: '',
      phone: '',
      date: '',
      startTime: '',
      endTime: '',
      notes: ''
    })
    setSubmitMessage('')
  }

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)
    setSubmitMessage('')

    try {
      const response = await fetch('/api/submit-booking', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          serviceType: selectedService
        })
      })

      const result = await response.json()

      if (result.success) {
        setSubmitMessage('Booking submitted successfully! We will contact you soon.')
        setTimeout(() => {
          closeBookingModal()
        }, 2000)
      } else {
        setSubmitMessage('Error submitting booking. Please try again.')
      }
    } catch (error) {
      console.error('Booking submission error:', error)
      setSubmitMessage('Error submitting booking. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="App">
      {/* Header */}
      <header className="header">
        <div className="container">
          <div className="logo">
            <span className="wave-icon">🎵</span>
            WAVE HOUSE
          </div>
          <nav className="nav">
            <a href="#home">Home</a>
            <a href="#services">Services</a>
            <a href="#about">About</a>
            <a href="#contact">Contact</a>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section id="home" className="hero">
        <div className="hero-content">
          <h1>Professional Recording Studio</h1>
          <p>State-of-the-art equipment and professional engineers to bring your music to life</p>
          <button className="cta-button" onClick={() => openBookingModal('studio-access')}>
            Book Studio Time
          </button>
        </div>
      </section>

      {/* Services Section */}
      <section id="services" className="services">
        <div className="container">
          <h2>Our Services</h2>
          <div className="services-grid">
            {services.map((service) => (
              <div key={service.id} className="service-card">
                <h3>{service.title}</h3>
                <p>{service.description}</p>
                <div className="price">{service.price}</div>
                <button 
                  className="book-button"
                  onClick={() => openBookingModal(service.id)}
                >
                  Book Now
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="about">
        <div className="container">
          <h2>About Wave House</h2>
          <p>
            Wave House is Los Angeles' premier recording studio, equipped with industry-standard 
            equipment and staffed by experienced professionals. We provide a creative environment 
            where artists can bring their musical visions to life.
          </p>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="contact">
        <div className="container">
          <h2>Contact Us</h2>
          <div className="contact-info">
            <div className="contact-item">
              <strong>Email:</strong> letswork@wavehousela.com
            </div>
            <div className="contact-item">
              <strong>Phone:</strong> (555) 123-4567
            </div>
            <div className="contact-item">
              <strong>Address:</strong> 123 Music Row, Los Angeles, CA 90028
            </div>
          </div>
        </div>
      </section>

      {/* Booking Modal */}
      {showBookingModal && (
        <div className="modal-overlay" onClick={closeBookingModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Book {services.find(s => s.id === selectedService)?.title}</h3>
              <button className="close-button" onClick={closeBookingModal}>×</button>
            </div>
            
            <form onSubmit={handleSubmit} className="booking-form">
              <div className="form-group">
                <label>Name *</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="form-group">
                <label>Email *</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="form-group">
                <label>Phone *</label>
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="form-group">
                <label>Date *</label>
                <input
                  type="date"
                  name="date"
                  value={formData.date}
                  onChange={handleInputChange}
                  min={new Date().toISOString().split('T')[0]}
                  required
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Start Time *</label>
                  <input
                    type="time"
                    name="startTime"
                    value={formData.startTime}
                    onChange={handleInputChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>End Time *</label>
                  <input
                    type="time"
                    name="endTime"
                    value={formData.endTime}
                    onChange={handleInputChange}
                    required
                  />
                </div>
              </div>

              <div className="form-group">
                <label>Additional Notes</label>
                <textarea
                  name="notes"
                  value={formData.notes}
                  onChange={handleInputChange}
                  rows="3"
                  placeholder="Any special requirements or notes..."
                />
              </div>

              {submitMessage && (
                <div className={`submit-message ${submitMessage.includes('Error') ? 'error' : 'success'}`}>
                  {submitMessage}
                </div>
              )}

              <div className="form-actions">
                <button type="button" onClick={closeBookingModal} className="cancel-button">
                  Cancel
                </button>
                <button type="submit" disabled={isSubmitting} className="submit-button">
                  {isSubmitting ? 'Submitting...' : 'Submit Booking'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default App

